from collisions import *
from data import *
from multiprocessing import Pool, cpu_count
from functools import partial
'''all helper functions contained in collisions.py'''
White_Default= Color( 1, 1, 1 )

def cast_ray( eyeRay, sphereList, ambientLight, lightSource, eyePoint ):
   closestSphere =  find_closest_sphere( sphereList, eyeRay )
   if closestSphere != None:
      point = closestSphere[1]
      sphere = closestSphere[0]
      trueNormal = sphere_normal_at_point( sphere, point )
      fakePoint = translate_point( point, trueNormal * 0.01 )
      #lightray = Ray( lightSource.pt, normalize_vector( vector_from_to( fakePoint, lightSource.pt ) ) )
      #light_visible = compare_sphere_to_light( sphereList, lightray, lightSource )
      #print diffuse
      sphereshade = sphere_ambient_finish( sphere, ambientLight )
    
      diffuse_and_intensity = sphere_diffuse_and_intensity( sphere, point, lightSource, sphereList, eyePoint )
      return sphereshade + diffuse_and_intensity 
   else:
      return White_Default

def sphere_diffuse_and_intensity( sphere, point, lightSource, sphereList, eyePoint ):
   fakePoint = fake_point_translate( sphere, point )
   temp = light_diffuse( sphere, point, fakePoint, lightSource )
   lightDiffuse = temp[0]
   Ldir = temp[1]
   if hidden_sphere( sphereList, point, lightSource, Ldir ) == False:
      if lightDiffuse <= 0:
         return Color( 0, 0, 0 )
      if find_closest_sphere( sphereList, Ray( fakePoint, Ldir ) ) != None:
         return Color( 0, 0, 0 )
      lightshade = sphere_lightpoint( sphere, lightSource, lightDiffuse )
      intensity = specular_value( eyePoint, point, sphere, lightSource, lightDiffuse )
      if intensity > 0:
         finalshade = lightshade + specular_shade( intensity, sphere, lightSource )
      else:
         finalshade = lightshade
      return finalshade
   return Color( 0, 0, 0 )

def cast_pixel( currentPoint, eyePoint, sphereList, ambientLight, lightSource ):
   currentVector = vector_from_to( eyePoint, currentPoint )
   currentRay = Ray( eyePoint, currentVector )
   currentColor = cast_ray( currentRay, sphereList, ambientLight, lightSource, eyePoint )
   color = convert_color( currentColor )
   return color.raw_str()

# Takes the viewpoint and resolution and computes a list of actual pixels to render
def compute_pixel_list( minX, minY, maxX, maxY, width, height ):
   current_x = minX
   current_y = maxY
   step_x = ( maxX - minX ) / float( width )
   step_y = ( maxY - minY ) / float( height )
   pixel_list = []
   # need to go from top to bottom
   while current_y > minY :
      pixel_row = []
      while current_x < maxX :
         pixel_row.append(Point(current_x, current_y, 0))
         current_x += step_x
      pixel_list.extend(pixel_row)
      current_x = minX
      current_y -= step_y
   return pixel_list

# This is the main function that actually computes all the ray casting
def cast_all_rays( minX, maxX, minY, maxY, 
                  width, height, eyePoint, sphereList, ambientLight, lightSource ):
   pixel_results = []
   
   multi = False
   print "Using {} threads".format( cpu_count() )
   if multi:
      pixel_list = compute_pixel_list( minX, minY, maxX, maxY, width, height )
      
      p = Pool() # left blank to default to cpu_count()
      partial_func = partial(cast_pixel, 
                             eyePoint = eyePoint, 
                             sphereList = sphereList,
                             ambientLight = ambientLight,
                             lightSource = lightSource)

      pixel_results = p.map(partial_func, pixel_list)
   else:
      pixel_list = compute_pixel_list( minX, minY, maxX, maxY, width, height )
      for currentPoint in pixel_list:
         currentVector = vector_from_to( eyePoint, currentPoint )
         currentRay = Ray( eyePoint, currentVector )
         currentColor = cast_ray( currentRay, sphereList, ambientLight, lightSource, eyePoint )
         color = convert_color( currentColor )
         pixel_results.append( color.raw_str() )
      return pixel_results
