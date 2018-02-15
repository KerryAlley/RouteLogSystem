#CopyCurrentData.py
#RouteLogSystem
#KAlley 2013_07_29 - Present
#GitHub started 2018_02_08
"""
This script sync's up the data driving the Route Log System (LocalData.gdb) with the original sources (generally on VTrans SDE servers).
The names of files in LocalData.gdb are changed to match expected names preserved in the Route Log System template mxd.  Using the filenames
         in LocalData.gdb alone to guess the source might be misleading, as the name might reflect a working copy rather than a published copy.
         (e.g. rdsmall_arc might be copy of Trans_RDS, which is the published version of rdsmall_arc, and therefore doesn't have recent edits.)

CALLED BY: RoutelogDataPreProcessing.py
CALLS: NA
INPUTS: Data sets of various types: ArcGIS Feature Classes and Tables, Excel Tables, Access Tables, .txt Files
OUTPUTS: Copies of all datasets into LocalDataPath
"""

import arcpy, os, sys
arcpy.env.overwriteOutput = True

def MainScript(LocalDataPath, rootPath):
    #LocalDataPath = r"V:\Projects\Shared\RouteLogSystem\ArcGIS_10_Prototype\Prototype_V10\LocalData.gdb"
    workspace = arcpy.env.workspace
    ReferenceLinesGDB = os.path.join(rootPath, "ReferenceLines.gdb")


    ##################################
    ##Tables and FeatureClasses on V:\
    ##################################

    #NOTE: SINVENT_LRS table is created in RoutelogDataPreProcessing.py

    #DataSource = r"V:\Projects\Shared\Mapping\RouteLogSystem\ArcGIS_10_RouteLogSystem\LocalDataFiles\SINVENT_LRS.mdb\SINVENT_PRIM_QDB_2017"
    #NewName = "SINVENT_PRIM_QDB"
    #arcpy.TableToTable_conversion(DataSource, LocalDataPath, NewName)

    #DataSource = r"V:\Projects\Shared\Mapping\RouteLogSystem\ArcGIS_10_RouteLogSystem\LocalDataFiles\SINVENT_LRS.mdb\SINVENT_SHORT_QDB_2017"
    #NewName = "SINVENT_SHORT_QDB"
    #arcpy.TableToTable_conversion(DataSource, LocalDataPath, NewName)


    DataSource = r"V:\Projects\Shared\Mapping\RouteLogSystem\ArcGIS_10_RouteLogSystem\Transtruc\Transtruc_LRS.gdb\Structures_LRS_XY"
    NewName = "Structures_LRS_XY"
    arcpy.TableToTable_conversion(DataSource, LocalDataPath, NewName)

    DataSource = os.path.join(r"V:\Projects\Shared\Mapping\RouteLogSystem\ArcGIS_10_RouteLogSystem_2017_09_21\LocalData.gdb", "RR_Xing_point_LRS_GDBGEN_join")
    NewName = "RR_Xing_point_LRS_GDBGEN_join"
    NewName = "RR_Xing_point"
    arcpy.TableToTable_conversion(DataSource, LocalDataPath, NewName)

    DataSource = r"V:\Projects\Shared\Mapping\RouteLogData_Master\MATS_UnitTable.mdb\MATS_UnitTable_20130325"
    NewName = "District_Lookup"
    arcpy.TableToTable_conversion(DataSource, LocalDataPath, NewName)

    DataSource = os.path.join(rootPath, r"LocalDataFiles\AADTWarehouse2016RevB.xlsx")
    NewName = "AADT_Data"
    arcpy.ExcelToTable_conversion(DataSource, os.path.join(LocalDataPath, NewName))

    DataSource = os.path.join(rootPath, r"LocalDataFiles\StationListingForMapping100317.xlsx")
    TempName = "TrafficCountersTemp"
    NewName = "TrafficCounters"
    arcpy.ExcelToTable_conversion(DataSource, os.path.join(LocalDataPath, TempName))
    query = "LRS IS NOT NULL AND (Y2015 IS NOT NULL OR Y2014 IS NOT NULL OR Y2013 IS NOT NULL OR Y2012 IS NOT NULL OR Y2016 IS NOT NULL)"
    arcpy.TableToTable_conversion(os.path.join(LocalDataPath,TempName), LocalDataPath, NewName, query)

    #DataSource = os.path.join(rootPath, r"LocalDataFiles\StationListing092316.csv")
    #TempName = "TrafficCountersTemp"
    #NewName = "TrafficCounters"
    #arcpy.TableToTable_conversion(DataSource, LocalDataPath, TempName)
    #query = "LRS IS NOT NULL AND (Y2015 IS NOT NULL OR Y2014 IS NOT NULL OR Y2013 IS NOT NULL OR Y2012 IS NOT NULL OR Y2011 IS NOT NULL)"
    #arcpy.TableToTable_conversion(os.path.join(LocalDataPath,TempName), LocalDataPath, NewName, query)

    DataSource = r"V:\Projects\Shared\HighwayResearch\HighCrashLocations\2012-2016 HCL Mapping\Map Formal HCL 2012-2016 Sections.xlsx"
    NewName = "HighCrashLocations"
    arcpy.ExcelToTable_conversion(DataSource, os.path.join(LocalDataPath, NewName))
    
    DataSource = r"V:\Projects\Shared\Mapping\RouteLogSystem\ArcGIS_10_RouteLogSystem\LocalDataFiles\Map HCL 2012-2016"
    NewName = "HighCrashIntersections"
    arcpy.ExcelToTable_conversion(DataSource, os.path.join(LocalDataPath, NewName))
    
    ##################################
    ##Feature Classes on GDB_HMS:
    ##################################
    DataSource = r"Database Connections\GDB_HMS.sde\GDB_HMS.HMSADMIN.Boundaries\GDB_HMS.HMSADMIN.FAU_Boundaries_2014"
    NewName = "FAU_Boundaries"
    arcpy.FeatureClassToFeatureClass_conversion(DataSource, LocalDataPath, NewName)

    #DataSource = r"Database Connections\GDB_HMS.sde\GDB_HMS.HMSADMIN.HighwayMappingSystem\GDB_HMS.HMSADMIN.transtruc_HMS_point"
    #NewName = "transtruc"
    #arcpy.FeatureClassToFeatureClass_conversion(DataSource, LocalDataPath, NewName)

    DataSource = r"Database Connections\GDB_HMS.sde\GDB_HMS.HMSADMIN.HighwayMappingSystem\GDB_HMS.HMSADMIN.rdsmall_arc"
    NewName = "rdsmall_hms"
    arcpy.FeatureClassToFeatureClass_conversion(DataSource, LocalDataPath, NewName)

    DataSource = r"Database Connections\GDB_HMS.sde\GDB_HMS.HMSADMIN.RTLOGPTS"
    NewName = "rtlogpts"
    #query = "USEFORRTLG = 'Y'"
    arcpy.FeatureClassToFeatureClass_conversion(DataSource, LocalDataPath, NewName)


    ##################################
    ##Tables on GDB_HMS:
    ##################################
    DataSource = r"Database Connections\GDB_HMS.sde\GDB_HMS.HMSADMIN.MasterRouteDefinition"
    NewName = "MasterRouteDefinition"
    arcpy.TableToTable_conversion(DataSource, LocalDataPath, NewName)

    DataSource = r"Database Connections\GDB_HMS.sde\GDB_HMS.HMSADMIN.CURVE"
    NewName = "CURVE"
    arcpy.TableToTable_conversion(DataSource, LocalDataPath, NewName)

    DataSource = r"Database Connections\GDB_HMS.sde\GDB_HMS.HMSADMIN.GRADE"
    NewName = "CurveGrade"
    arcpy.TableToTable_conversion(DataSource, LocalDataPath, NewName)

    DataSource = r"Database Connections\GDB_HMS.sde\GDB_HMS.HMSADMIN.BASE"
    NewName = "RoadWidth"
    arcpy.TableToTable_conversion(DataSource, LocalDataPath, NewName)

    DataSource = r"Database Connections\GDB_HMS.sde\GDB_HMS.HMSADMIN.NHS"
    NewName = "NHS"
    arcpy.TableToTable_conversion(DataSource, LocalDataPath, NewName)

    #Old data?
    #DataSource = r"Database Connections\GDB_HMS.sde\GDB_HMS.HMSADMIN.FAULimit"
    #NewName = "FAULimit"
    #arcpy.TableToTable_conversion(DataSource, LocalDataPath, NewName)

    #Only grab Urban Area records
    DataSource = r"Database Connections\GDB_HMS.sde\GDB_HMS.HMSADMIN.Urban_Code"
    NewName = "UrbanCode"
    arcpy.TableToTable_conversion(DataSource, LocalDataPath, NewName, "UAName IS NOT NULL AND UAName <> '-'")

    #DataSource = r"Database Connections\GDB_HMS.sde\GDB_HMS.HMSADMIN.FUNCCLASS"
    #NewName = "FUNCCLASS"
    #arcpy.TableToTable_conversion(DataSource, LocalDataPath, NewName)

    DataSource = r"Database Connections\GDB_HMS.sde\GDB_HMS.HMSADMIN.FunctionalClass"
    NewName = "FUNCCLASS"
    arcpy.TableToTable_conversion(DataSource, LocalDataPath, NewName)

    DataSource = r"Database Connections\GDB_HMS.sde\GDB_HMS.HMSADMIN.FUNCL_Lookup"
    NewName = "FUNCL_Lookup"
    arcpy.TableToTable_conversion(DataSource, LocalDataPath, NewName)

    DataSource = r"Database Connections\GDB_HMS.sde\GDB_HMS.HMSADMIN.HISTORICPROJECTS"
    NewName = "HISTORICPROJECTS"
    arcpy.TableToTable_conversion(DataSource, LocalDataPath, NewName)

    DataSource = r"Database Connections\GDB_HMS.sde\GDB_HMS.HMSADMIN.ROADWIDTH_HPMS"
    NewName = "ROADWIDTH_HPMS"
    arcpy.TableToTable_conversion(DataSource, LocalDataPath, NewName)

    DataSource = r"Database Connections\GDB_HMS.sde\GDB_HMS.HMSADMIN.TOWN_CENTER"
    NewName = "TOWN_CENTER"
    arcpy.TableToTable_conversion(DataSource, LocalDataPath, NewName)

    DataSource = r"Database Connections\GDB_HMS.sde\GDB_HMS.HMSADMIN.VILLUC"
    NewName = "VILLUC"
    arcpy.TableToTable_conversion(DataSource, LocalDataPath, NewName)

    DataSource = r"Database Connections\GDB_HMS.sde\GDB_HMS.HMSADMIN.LIMITEDACCESS"
    NewName = "LIMITEDACCESS"
    arcpy.TableToTable_conversion(DataSource, LocalDataPath, NewName)

    DataSource = r"Database Connections\GDB_HMS.sde\GDB_HMS.HMSADMIN.MRD_LRS_CHANGEHISTORY"
    NewName = "MRD_LRS_CHANGEHISTORY"
    arcpy.TableToTable_conversion(DataSource, LocalDataPath, NewName)



    ##################################
    ##Tables on GDB_GEN:
    ##################################
    #DataSource = r"Database Connections\GDB_Gen.sde\GDB_Gen.VTrans_Admin.SINVENT_PRIM"
    #NewName = "SINVENT_PRIM"
    #arcpy.TableToTable_conversion(DataSource, LocalDataPath, NewName)

    #DataSource = r"Database Connections\GDB_Gen.sde\GDB_Gen.VTrans_Admin.SINVENT_SEC"
    #NewName = "SINVENT_SEC"
    #arcpy.TableToTable_conversion(DataSource, LocalDataPath, NewName)

    #DataSource = r"Database Connections\GDB_Gen.sde\GDB_Gen.VTrans_Admin.SCI_CULVERT_LOC"
    #NewName = "SCI_CULVERT_LOC"
    #arcpy.TableToTable_conversion(DataSource, LocalDataPath, NewName)



    ##################################
    ##Feature Classes on GDB_GEN:
    ##################################
    DataSource = r"Database Connections\GDB_Gen.sde\GDB_Gen.VTRANS_ADMIN.Boundary_Town"
    NewName = "townindex"
    arcpy.FeatureClassToFeatureClass_conversion(DataSource, LocalDataPath, NewName)

    DataSource = r"Database Connections\GDB_Gen.sde\GDB_Gen.VTRANS_ADMIN.Boundary_County"
    NewName = "Boundary_County"
    arcpy.FeatureClassToFeatureClass_conversion(DataSource, LocalDataPath, NewName)

    #DataSource = r"Database Connections\GDB_Gen.sde\GDB_Gen.VTRANS_ADMIN.HighwayShields"
    #NewName = "HighwayShields"
    #arcpy.FeatureClassToFeatureClass_conversion(DataSource, LocalDataPath, NewName)

    DataSource = r"Database Connections\GDB_Gen.sde\GDB_Gen.VTRANS_ADMIN.MATS_District_Mileages"
    NewName = "MATS_District_Mileages"
    arcpy.FeatureClassToFeatureClass_conversion(DataSource, LocalDataPath, NewName)

    DataSource = r"Database Connections\GDB_Gen.sde\GDB_Gen.VTRANS_ADMIN.Rail_LRS"
    NewName = "Rail_LRS"
    arcpy.FeatureClassToFeatureClass_conversion(DataSource, LocalDataPath, NewName)

    #DataSource = r"Database Connections\GDB_Gen.sde\GDB_Gen.VTRANS_ADMIN.Rail_Crossings"
    #NewName = "Rail_Crossings"
    #arcpy.FeatureClassToFeatureClass_conversion(DataSource, LocalDataPath, NewName)

    DataSource = r"Database Connections\GDB_Gen.sde\GDB_Gen.VTRANS_ADMIN.Assets_Signals"
    NewName = "Signals"
    arcpy.FeatureClassToFeatureClass_conversion(DataSource, LocalDataPath, NewName)

    #DataSource = r"Database Connections\GDB_Gen.sde\GDB_Gen.VTRANS_ADMIN.RTLOGPTS"
    #NewName = "rtlogpts"
    #arcpy.FeatureClassToFeatureClass_conversion(DataSource, LocalDataPath, NewName)

    #DataSource = r"Database Connections\GDB_Gen.sde\GDB_Gen.VTRANS_ADMIN.SCI_DI_MST"
    #NewName = "SCI_DI_MST"
    #arcpy.TableToTable_conversion(DataSource, LocalDataPath, NewName)

    DataSource = r"Database Connections\GDB_Gen.sde\GDB_Gen.VTRANS_ADMIN.TransRoad_MilePoints"
    NewName = "MilePoints"
    arcpy.FeatureClassToFeatureClass_conversion(DataSource, LocalDataPath, NewName)

    DataSource = r"Database Connections\GDB_Gen.sde\GDB_Gen.VTRANS_ADMIN.SPEEDZONES"
    NewName = "SPEEDZONES"
    arcpy.FeatureClassToFeatureClass_conversion(DataSource, LocalDataPath, NewName)

    DataSource = r"Database Connections\GDB_Gen.sde\GDB_Gen.VTRANS_ADMIN.Trans_LRS_Route_ete"
    NewName = "lrs_route_ete"
    arcpy.FeatureClassToFeatureClass_conversion(DataSource, os.path.join(rootPath,"ReferenceLines.gdb"), NewName)

    DataSource = r"Database Connections\GDB_Gen.sde\GDB_Gen.VTRANS_ADMIN.Trans_LRS_Route_twn"
    NewName = "lrs_route_twn"
    arcpy.FeatureClassToFeatureClass_conversion(DataSource, os.path.join(rootPath,"ReferenceLines.gdb"), NewName)

    DataSource = r"Database Connections\GDB_Gen.sde\GDB_Gen.VTRANS_ADMIN.Trans_RDS"
    NewName = "rdsmall_arc"
    arcpy.FeatureClassToFeatureClass_conversion(DataSource, LocalDataPath, NewName)

    DataSource = r"Database Connections\GDB_GEN.sde\GDB_Gen.VTRANS_ADMIN.Mapping_CustomerServiceLevels"
    NewName = "CustomerServiceLevels"
    arcpy.FeatureClassToFeatureClass_conversion(DataSource, LocalDataPath, NewName)

    DataSource = r"Database Connections\GDB_GEN.sde\GDB_Gen.VTRANS_ADMIN.CrashCurrent"
    NewName = "Crash2016"
    arcpy.FeatureClassToFeatureClass_conversion(DataSource, LocalDataPath, NewName)

    #DataSource = r"Database Connections\GDB_GEN.sde\GDB_Gen.VTRANS_ADMIN.AADT"
    #NewName = "AADT_Current"
    #arcpy.FeatureClassToFeatureClass_conversion(DataSource, LocalDataPath, NewName)


    ##################################
    ##Feature Classes on GDB_Hist:
    ##################################

    DataSource = r"Database Connections\GDB_HIST.sde\GDB_Hist.VTRANS_ADMIN.Crash2015"
    NewName = "Crash2015"
    arcpy.FeatureClassToFeatureClass_conversion(DataSource, LocalDataPath, NewName)

    DataSource = r"Database Connections\GDB_HIST.sde\GDB_Hist.VTRANS_ADMIN.Crash2014"
    NewName = "Crash2014"
    arcpy.FeatureClassToFeatureClass_conversion(DataSource, LocalDataPath, NewName)

    DataSource = r"Database Connections\GDB_HIST.sde\GDB_Hist.VTRANS_ADMIN.Crash2013"
    NewName = "Crash2013"
    arcpy.FeatureClassToFeatureClass_conversion(DataSource, LocalDataPath, NewName)

    DataSource = r"Database Connections\GDB_HIST.sde\GDB_Hist.VTRANS_ADMIN.Crash2012"
    NewName = "Crash2012"
    arcpy.FeatureClassToFeatureClass_conversion(DataSource, LocalDataPath, NewName)



    ##################################
    ##Feature Classes were on GDB_WEB:
    ##################################


    ##DataSource = r"Database Connections\GDB_WEB.sde\GDB_Web.RLSUSER.RailroadData\GDB_Web.RLSUSER.RR_Xing_point"
    #DataSource = r"V:\Projects\Shared\Mapping\RouteLogSystem\ArcGIS_10_RouteLogSystem_2016_09_23\LocalData.gdb\RR_Xing_point_LRS_GDBGEN_join"
    #NewName = "RR_Xing_point_LRS_GDBGEN_join"
    #NewName = "RR_Xing_point"
    #arcpy.TableToTable_conversion(DataSource, LocalDataPath, NewName)


    ##################################
    ##Feature Classes on GDB_VCGI:
    ##################################
    #Still used to get stream names
    DataSource = r"Database Connections\GDB_VCGI.sde\GDB_VCGI.VCGI_ADMIN.Water_VHDCARTO_line"
    NewName = "VHDCARTO_line"
    arcpy.FeatureClassToFeatureClass_conversion(DataSource, LocalDataPath, NewName)

    DataSource = r"Database Connections\GDB_VCGI.sde\GDB_vcgi.VCGI_ADMIN.WaterHydro_LKCH5K\GDB_VCGI.VCGI_ADMIN.Water_LKCH5K_poly"
    NewName = "LKCH5K"
    arcpy.FeatureClassToFeatureClass_conversion(DataSource, LocalDataPath, NewName)
