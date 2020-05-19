#! /usr/bin/env python3
#
def quad_mpi ( ):

    #*****************************************************************************80
    #
    ## QUAD_MPI estimates an integral using a quadrature rule.
    #
    #  Licensing:
    #
    #    This code is distributed under the GNU LGPL license.
    #
    #  Modified:
    #
    #    25 October 2011
    #
    #  Author:
    #
    #    John Burkardt
    #
    import numpy as np
    import sys
    import platform
    from mpi4py import MPI
    from math import fabs

    comm = MPI.COMM_WORLD

    id = comm.Get_rank()

    p = comm.Get_size()

    a =  0.0
    b = 10.0
    exact = 0.49936338107645674464
    #
    #  Assume process 0 decides on the value of N, and sends it to others.
    #
    if id == 0:
      n = np.array ( 10000, dtype = 'i' )
      wtime = MPI.Wtime ( )
      print ( '' )
      print ( 'QUAD_MPI' )
      print ( '  Python version: %s' % ( platform.python_version ( ) ) )
      print ( '  Estimate an integral of f(x) from A to B.' )
      print ( '  f(x) = 50 / (pi * ( 2500 * x * x + 1 ) )' )
      print ( '' )
      print ( '  A        = %g' % ( a ))
      print ( '  B        = %g' % ( b ))
      print ( '  N        = %d' % ( n ))
      print ( '  Exact    = %g' % ( exact ))
      print ( '' )
      print ( '  Use MPI to divide the computation among' )
      print ( '  multiple processes.' )
    else:
      n = np.array ( 0, dtype = 'i' )

    comm.Bcast ( [ n, MPI.INT ], root = 0 )

    t = np.array ( 0.0, dtype = 'd' )

    for i in range ( id, n, p ):
      x = ( float ( n - i - 1 ) * a + float ( i ) * b ) / float ( n - 1 )
      t = t + f ( x )

    print ( '  Sum for process %d is %g' % ( id, t ))

    total = np.array ( 0.0, 'd' )

    comm.Reduce ( [ t, MPI.DOUBLE ], [ total, MPI.DOUBLE ], op = MPI.SUM, root = 0 )

    if id == 0:
      wtime = MPI.Wtime ( ) - wtime

      total = ( b - a ) * total / float ( n )
      error = fabs ( total - exact )

      print ( '' )
      print ( '  Estimate = ', total )
      print ( '  Error    = ', error )
      print ( '  Time     = ', wtime )
    #
    #  Terminate.
    #
      print ( '' )
      print ( 'QUAD_MPI:' )
      print ( '  Normal end of execution.' )
      return

def f ( x ):

    #*****************************************************************************80
    #
    ## F evaluates the function.
    #
    #  Licensing:
    #
    #    This code is distributed under the GNU LGPL license.
    #
    #  Modified:
    #
    #    26 October 2012
    #
    #  Author:
    #
    #    John Burkardt
    #
    import numpy as np

    value = 50.0 / ( np.pi * ( 2500.0 * x * x + 1.0 ) );

    return value

def timestamp ( ):

    #*****************************************************************************80
    #
    ## TIMESTAMP prints the date as a timestamp.
    #
    #  Licensing:
    #
    #    This code is distributed under the GNU LGPL license. 
    #
    #  Modified:
    #
    #    06 April 2013
    #
    #  Author:
    #
    #    John Burkardt
    #
    #  Parameters:
    #
    #    None
    #
    import time

    t = time.time ( )
    print ( time.ctime ( t ) )

    return None

def timestamp_test ( ):

    #*****************************************************************************80
    #
    ## TIMESTAMP_TEST tests TIMESTAMP.
    #
    #  Licensing:
    #
    #    This code is distributed under the GNU LGPL license. 
    #
    #  Modified:
    #
    #    03 December 2014
    #
    #  Author:
    #
    #    John Burkardt
    #
    #  Parameters:
    #
    #    None
    #
    import platform

    print ( '' )
    print ( 'TIMESTAMP_TEST:' )
    print ( '  Python version: %s' % ( platform.python_version ( ) ) )
    print ( '  TIMESTAMP prints a timestamp of the current date and time.' )
    print ( '' )

    timestamp ()
    #
    #  Terminate.
    #
    print ( '' )
    print ( 'TIMESTAMP_TEST:' )
    print ( '  Normal end of execution.' )
    return

if ( __name__ == '__main__' ):
  timestamp ( )
  quad_mpi ( )
  timestamp ( )

