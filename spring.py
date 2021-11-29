import numpy as np

class Spring:
    """
    Class for tracking the motion of an object (the face) using damped spring forces. 
    Simple Euler update scheme is used to compute each time step for position and velocity. 

    Parameters
    ----------
    x : 1x2 numpy array, float64
        Initial position of the camera.
    v : 1x2 numpy array, float64, optional
        Initial velocity of the camera. (default [0., 0.,])
    k : float64, optional
        Spring constant. Larger values means stronger force to follow the origin. (default 1.)
    gamma : float64, optional
        Damping constant. Larger values means velocity decays faster. (default 1.)
    t_step : float64, optional
        Time step at each update. (default 1e-1)

    Attributes
    ----------
    x : 1x2 numpy array, float64
        Position of the camera 
    orig : 1x2 numpy array, float64
        Position of the spring origin, determines the direction of the force on the camera.
    v : 1x2 numpy array, float64
        Initial velocity of the camera.
    k : float64
        Spring constant. Larger values means stronger force to follow the origin.
    gamma : float64
        Damping constant. Larger values means velocity decays faster.
    t_step : float64
        Time step at each update.

    Methods
    -------
    set_spring(orig : 1x2 numpy array (float64))
        Set the origin position of the spring.
    get_x() -> x : 1x2 numpy array (int64)
        Return an integer representation of the current position vector.
    update() 
        Update current position and velocity vectors using Euler update scheme
        and the given parameters. Calls get_acc().
    _get_acc() -> a : 1x2 numpy array (float64)
        Calculate the current acceleration using a damped spring ODE.
    """
    def __init__(self, x, v = np.array([0., 0.]), k = 1, gamma = 1, t_step = 1e-1):
        self.x, self.v, self.k, self.gamma, self.t_step = x, v, k, gamma, t_step
        self.orig = x

    def set_spring(self, orig):
        """Set the origin position of the spring.
        Parameters
        ----------
        orig : 1x2 numpy array, float64
            Position vector of the spring origin.
        """
        self.orig = orig

    def get_x(self):
        """Return the current position vector as an integer.
        Returns
        -------
        x_int : 1x2 numpy array, int64
            Current position vector as a rounded integer.
        """
        return np.int64(np.round(self.x))

    def _get_acc(self):
        """Compute acceleration given the damped spring ODE.
        Returns
        -------
        a : 1x2 numpy array, float64
            Acceleration vector.
        """
        a = -1 * self.k * (self.x - self.orig) - self.gamma * self.v
        return a

    def update(self):
        """Update position and velocity vectors using Euler update scheme."""
        a = self._get_acc()
        self.x += self.v * self.t_step + 0.5 * a * self.t_step ** 2
        self.v += a * self.t_step

def main():
    global s
    s = Spring(np.array([0., 0.]))
    s.set_spring(np.array([1., 0.]))
    s.get_acc()
    s.update()
    print(s.x, s.v)

if __name__ == '__main__':
    main()
