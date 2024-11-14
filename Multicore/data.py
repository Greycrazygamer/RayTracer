def epsilon_equal( n, m, epsilon=0.00001 ):
   return ( n - epsilon ) < m and ( n + epsilon > m )

class Point( object ):
   def __init__( self, x, y, z ):
      self.x = x
      self.y = y
      self.z = z
   
   def __str__( self ):
      return "Pt< {}, {}, {} >".format( self.x, self.y, self.z  )
   
   def __eq__( self, other ):
      return ( epsilon_equal( self.x, other.x ) 
          and epsilon_equal( self.y, other.y ) 
          and epsilon_equal( self.z, other.z ) ) 

   def __repr__(self):
      return self.__str__()

class Vector( object ):
   def __init__( self, x, y, z ):
      self.x = x
      self.y = y
      self.z = z
   
   def __str__( self ):
      return "Vtr< {}, {}, {} >".format( self.x, self.y, self.z  )
   
   def __eq__( self, other ):
      return ( epsilon_equal( self.x, other.x ) 
       and epsilon_equal( self.y, other.y ) 
       and epsilon_equal( self.z, other.z ) ) 
   
   def __add__( self, other):
      x = self.x + other.x
      y = self.y + other.y
      z = self.z + other.z
      return Vector( x, y, z )

   def __mul__(self, other):
      # Vector * Vector == Dot Product (return float)
      if isinstance(other, self.__class__):
         x = self.x * other.x 
         y = self.y * other.y 
         z = self.z * other.z
         newdot = x + y + z
         return newdot
      # Vector * Scalar == (return Vector)
      elif isinstance(other, int) or isinstance(other, float):
         x = self.x * other
         y = self.y * other
         z = self.z * other
         return Vector( x, y, z ) 
      else:
         raise TypeError("unsupported operand type(s) for +: '{}' and '{}'").format(self.__class__, type(other))

class Ray( object ):
   def __init__( self, pt, dir ):
      self.pt = pt
      self.dir = dir
   
   def __eq__( self, other ):
      return ( epsilon_equal( self.pt.x, other.pt.x )
          and epsilon_equal( self.pt.y, other.pt.y )
          and epsilon_equal( self.pt.z, other.pt.z ) 
          and  Vector.__eq__( self.dir, other.dir ) )
   def __str__( self ):
      return "Ray< pt:{}, dir:{} >".format( self.pt, self.dir  ) 

class Color( object ):
   def __init__( self, r, g, b ):
      self.r = r
      self.g = g
      self.b = b
   
   def __eq__( self, other ):
      return ( epsilon_equal( self.r, other.r ) 
          and epsilon_equal( self.g, other.g )
          and epsilon_equal( self.b, other.b ) ) 
   
   def __add__( self, other):
      r = self.r + other.r
      g = self.g + other.g
      b = self.b + other.b
      return Color( r, g, b )

   def __str__( self ):
      return "Color< {}, {}, {} >".format( self.r, self.g, self.b  )
   
   def raw_str( self ):
      return "{} {} {}\n".format( self.r, self.g, self.b )
   
   def __repr__(self):
      return self.__str__()
   


class Sphere( object ):
   def __init__( self, center, radius, color, finish ):
      self.center = center
      self.radius = radius
      self.color = color
      self.finish = finish
   
   def __str__( self ):
      return "Sphr< ctr:{}, rad:{} >".format( self.center, self.radius  ) 
   def __repr__(self):
      return self.__str__()

   def __eq__( self, other ):
      return ( Point.__eq__( self.center, other.center ) 
       and epsilon_equal( self.radius, other.radius )
       and Color.__eq__( self.color, other.color )
       and Finish.__eq__( self.finish, other.finish ) ) 

class Finish( object ):
    def __init__( self, ambience, diffuse, specular, roughness ):
      self.ambience = ambience
      self.diffuse = diffuse
      self.specular = specular
      self.roughness = roughness
    
    def __eq__( self, other ):
    	return ( epsilon_equal( self.ambience, other.ambience ) and 
  	      epsilon_equal( self.diffuse, other.diffuse ) and
          epsilon_equal( self.specular, other.specular ) and
          epsilon_equal( self.roughness, other.roughness ) )

class Light( object ):
   def __init__( self, pt, color ):
      self.pt = pt
      self.color = color
   
   def __eq__( self, other ):
      return ( Point.__eq__( self.pt, other.pt )
         and Color.__eq__( self.color, other.color ) )
