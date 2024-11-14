#!/usr/bin/python
from cast import *
import commandline as cmd
import sys

def open_file( name, mode ):
   try: 
      return open( name[1], mode )
   except:
      print "Error: missing file to read"
      sys.exit()

def write_to_file( width, height, pixel ):
   with open( 'image.ppm', 'w' ) as file:
      file.write( 'P3\n' + str( width ) + ' ' + str( height ) + '\n255\n' )
      file.write( ''.join( pixel ) )

def get_spherelist_from_file( argv ):
   sphereFile = open_file( argv, 'r' )
   result = []
   for lineNum, line in enumerate( sphereFile, 1 ):
      linelist = line.split()
      if linelist == []:
         print "Error: No Values in Line " + str( lineNum ) + "... skipping"
         continue
      if len( linelist ) != 11:
         print "Error: Incorrect Num of Values in Line " + str( lineNum ) + "... skipping"
         continue

      try:
         x = float(linelist[0])
         y = float(linelist[1])
         z = float(linelist[2])
         radius = float(linelist[3])
         r = float(linelist[4])
         g = float(linelist[5])
         b = float(linelist[6])
         sphere = Sphere( Point( x, y, z ), radius, Color( r, g, b ) )
         
         ambient = float(linelist[7])
         diffuse = float(linelist[8])
         specular = float(linelist[9])
         roughness = float(linelist[10])
         finish = Finish( ambient, diffuse, specular, roughness )
         result.append( ( sphere, finish ) )
      
      except:
         print "Error: Malformed Sphere on Line " + str( lineNum ) + "... skipping"
         continue
   sphereFile.close 
   return result
   
def main( argv ):
   arg_list = cmd.commands( argv )
   view = arg_list[0]
   width = view[4]
   height = view[5]
   eye_point = arg_list[1]
   sphere_list = get_spherelist_from_file( argv )
   ambient_light = arg_list[2]
   lightsource = arg_list[3]
   pixel_results = cast_all_rays(view[0], view[1], view[2], view[3], width, height,
      eye_point, sphere_list, ambient_light, lightsource)
   write_to_file( int( width ), int( height ), pixel_results )
   
if __name__=='__main__':
   main( sys.argv )
