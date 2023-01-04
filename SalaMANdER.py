"""
SalaMANdER: Solid Mechanics And Nonlinear Elasticity Routines
---------------------------------------------------------------------
This module contains routines for nonlinear solid mechanics formulations for 
use in FEniCS (www.fenicsproject.org) scripts.

The intent here is rapid prototyping of new material models through a subclass
of MaterialModel that implements a constructor and the interiorResidual method.
That way, the other items common to nearly all solid formulations do not have
to be duplicated for each new material model.
"""
from abc import ABC, abstractmethod
from dolfin import *

def bulkModulus(E,nu):
    """ Convert a Young's modulus and a Poisson's ratio to a bulk modulus."""
    return firstLameParameter(E,nu) + 2/3*secondLameParameter(E,nu)

def shearModulus(E,nu):
    """ Convert a Young's modulus and a Poisson's ratio to a shear modulus."""
    return secondLameParameter(E,nu)

def firstLameParameter(E,nu):
    """ 
    Convert Young's modulus and Poisson's ratio to Lame's first parameter.
    """
    return E*nu/((1+nu)*(1-2*nu))

def secondLameParameter(E,nu):
    """ 
    Convert Young's modulus and Poisson's ratio to Lame's second parameter.
    """
    return E/(2*(1 + nu))


class MaterialModel(ABC):
    """
    The abstract base model for a material that includes the material 
    properties. This abstract class leaves the interiorResidual to each 
    subclass material.
    """

    def __init__(self,rho=Constant(0),**props):
        """
        Initiate a material model with a density ``rho`` and other material
        properites (Young's modulus, Poisson's ratio, etc) that are used by the
        concrete classes.
        """
        self.rho = rho
        self.props = props
        super().__init__()

    @abstractmethod
    def interiorResidual(self,u,v,dx=dx):
        pass

    def accelerationResidual(self,du_dtt,v,dx=dx):
        return self.rho*inner(du_dtt,v)*dx

    def massDampingResidual(self,du_dt,c,v,dx=dx):
        return self.rho*c*inner(du_dt,v)*dx

    def bodyforceResidual(self,f,v,dx=dx):
        return - self.rho*inner(f,v)*dx

    def tractionBCResidual(self,h,v,ds=ds):
        return - inner(v,h)*ds
    
    def penaltyWeakBCResidual(self,u,v,g,beta,ds=ds):
        return - inner(beta*(u-g),v)*ds

    def getBasicTensors(self,u):
        if not u.ufl_shape:
            nsd = 0
        else:
            nsd = u.ufl_shape[0]
        I = Identity(nsd)
        F = grad(u) + I
        J = det(F)
        C = F.T*F
        E = 0.5*(C-I)
        return I,F,J,C,E



class StVenantKirchoff(MaterialModel):
    """ 
    A St. Venant-Kirchoff material. 
    
    Requires material properties 'kappa' (bulk modulus) and 'mu' (shear
    modulus).
    """

    def interiorResidual(self,u,v,dx=dx):
        I,F,_,_,E = self.getBasicTensors(u)
        S = self.props['kappa']*tr(E)*I \
            + 2.0*self.props['mu']*(E - tr(E)*I/3.0)
        return inner(F*S,grad(v))*dx


class NeoHookean(MaterialModel):
    """ 
    A Neo-Hookean material from Wu et al. 2019. 
    
    Requires material properties 'kappa' (bulk modulus) and 'mu' (shear
    modulus).
    """

    def interiorResidual(self,u,v,S0=None,dx=dx):
        I,F,J,C,_ = self.getBasicTensors(u)
        nsd = tr(I)
        if (S0==None):
            S0 = Constant(0)*I
        S = self.props['mu']*(J**(-2/3))*(I-(tr(C) + (3-nsd))/3*inv(C)) \
            + self.props['kappa']/2*((J**2)-1)*inv(C)
        return inner(F*(S+S0),grad(v))*dx


class JacobianStiffening(MaterialModel):
    """ 
    Jacobian-based mesh stiffening. 
    
    Requires material property 'power' to define the strength of the
    stiffening.
    """

    def interiorResidual(self,u,v,J_M,dx=dx):
        I,F,J,_,E = self.getBasicTensors(u)
        fictitious_E = Constant(1.0)
        fictitious_nu = Constant(0.3)
        K = bulkModulus(fictitious_E/pow((J_M),self.props['power_J_M']),fictitious_nu)
        mu = shearModulus(fictitious_E/pow((J_M),self.props['power_J_M']),fictitious_nu)
        # K = K/pow(J,self.props['power_J'])
        # mu = mu/pow(J,self.props['power_J'])
        S = K*tr(E)*I + 2.0*mu*(E - tr(E)*I/3.0)
        return inner(F*S,grad(v))*dx