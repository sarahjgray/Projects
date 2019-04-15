#####LAB 3#######

#### PLEASE READ ###### PLEASE READ ######## PLEASE READ ######## PLEASE READ ########

# CHANGE THIS PATH (my_path) - This code is set up to work as long as the two folders I sent (GSR and NRC) are within the folder that you are using as a path. 
#This path should be changed to a folder that contains the GSR and NRC folders within it 
#an example path all the way to a shapefile would look like this -> r"C:\Users\darcym.UVIC\Desktop\data\GSR_HOSPITALS_SVW\HOSPITALS_point.shp"

my_path = r"C:\Users\darcym.UVIC\Desktop\data"

#Create new file gdb
name = r"\L3GDB.gdb"
gdb_path = my_path + name


# Execute CreateFileGDB
arcpy.CreateFileGDB_management(my_path, name)



#set workspace
arcpy.env.workspace = gdb_path



#Import my layers using feature class to feature class
import arcpy

hospitals = my_path + r"\GSR_HOSPITALS_SVW\HOSPITALS_point.shp"
PopulatedPlaces = my_path + r"\NRC_POPULATED_PLACES_1M_SP\POP_PL_1M_point.shp"
outLocation = gdb_path


OutClassname = "hospitals"
OutClass2name = "Populated_Places"
arcpy.FeatureClassToFeatureClass_conversion(hospitals, outLocation, OutClassname)
arcpy.FeatureClassToFeatureClass_conversion(PopulatedPlaces, outLocation, OutClass2name)

########TASK 3########

PopPlace = gdb_path + "\\Populated_Places"
EstPop = "EST_POP"
CityNames = "Name"
city = "Comox"

print ("Task 3 Complete")

########### TASK 4############
#Use search cursor to calcuclate average population size 
average = 0
totalPopulation = 0
recordsCounted = 0

with arcpy.da.SearchCursor(PopPlace, (EstPop)) as cursor:
	for row in cursor:
		totalPopulation += row[0]
		recordsCounted += 1
 
average = totalPopulation / recordsCounted
print ("Average population for all cities is " + str(average))
print ("Task 4 Complete")
 
#Average population for all cities is 3096.4995586937334

#######TASK 5########
ComoxPop = 0
arcpy.analysis.Near(PopPlace, hospitals)
near = "NEAR_DIST"
fields = [CityNames, EstPop, near]
minPop = 0.9*int(ComoxPop)
maxPop = 1.1*int(ComoxPop)
with arcpy.da.SearchCursor(PopPlace, fields) as cursor:
	for row in cursor:
		if row[0] == city:
			ComoxPop += row[1] #Near function
			print('Town name =',row[0], 'Population =',row[1], 'Distance to hospital =',row[2])
			minPop = 0.9*int(ComoxPop)
			maxPop = 1.1*int(ComoxPop)
			print(minPop, maxPop)
		


print("Task 5 Complete")
			

##### TASK 6 #######
distavg = 0 
records2 = 0
with arcpy.da.SearchCursor(PopPlace, fields) as cursor:
	for row in cursor:
		if (row[1] >= minPop) & (row[1] <= maxPop):
			distavg += row[2]
			records2 += 1
			print(row[0])
print(records2)
print(distavg)		
average = distavg / records2
print('The average distance to hospitals for the selected cities =', average)

print("Task 6 Complete")

##### TASK 7 #####
#Add fields
arcpy.management.AddField('Populated_Places', 'CitySize', 'TEXT')
arcpy.management.AddField('Populated_Places', 'Dist_To_Hosp', 'TEXT')
#Assign them to variables
CitySize = "CitySize"
dist = "Dist_To_Hosp"

Fields = [EstPop, CitySize]
with arcpy.da.UpdateCursor(PopPlace, Fields) as cursor:
	for row in cursor:
		if row[0] <= 500:	
			row[1] = "Small"
		elif row[0] > 500 and row[0] <= 10000:
			row[1] = "Med"
		elif row[0] > 10000:
			row[1] = "Large"
	
		cursor.updateRow(row)

print('Halfway there, living on a prayer')

Fields2 = [near, dist]
with arcpy.da.UpdateCursor(PopPlace, Fields2) as cursor:
	for row in cursor:
		if row [0] <= 1000:
			row[1] = "Very Close"
		elif row[0] > 1000 and row[0] <= 10000:
			row[1] = "Close"
		elif row[0] > 10000:
			row[1] = "Far"
		
		cursor.updateRow(row)

print('Task 7 Complete')

###


#Name of my assigned City = Comox

#Average pop of all populated places in B.C. = 3096.4995586937334

#What is the population and distance to the nearest hospital of your assigned city 
# Town name = Comox, Population = 11636.0, Distance to hospital = 995.3265314535242

#What is the list of cities whose population is within +/- 10% of your assigned city’s population?
#Prince Rupert, Terrace, Sidney, Comox, Dawson Creek, Salmon Arm, Parksville, Aldergrove

#What is the average distance to the nearest hospital of those cities whose population is within +/- 10% of your assigned city’s population?
#The average distance to hospitals for the selected cities = 6676.933654525932

#MinPop = 10472.4
#MaxPop = 12799.6

#For the average, there are 8 places (including comox), and a neardist total of 53415.56923....