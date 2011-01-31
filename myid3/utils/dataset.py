"""
Author: Kostas Zoumpatianos
File: dataset.py
Description: Loads UCI datasets, only discrete values and without unknown values for the moment! :)
Date: March, 6 2010
"""
import string

class ContinuousDataSetException(Exception):
    def __str__(self):
        return "This dataset is continuous! This implementation cannot use it!"
        
class FieldValueNotValidException(Exception):
    def __str__(self):
        return "Not valid field value!"
        

class DataSet(object):
    fields = []
    records = []
    
    def __init__(self,names_filename=None, data_filename=None):
        data_file = open(data_filename, "r")
        
        if(names_filename != None):
            names_file = open(names_filename,"r")
            self.load_names(names_file)
        else:
            self.load_names_from_data(data_file)
        
        self.load_data(data_file,len(self.fields))
        
    def load_data(self,data_file, columns_number):
        for row_id,row in enumerate(data_file):
            
            if(string.strip(row) == ""):
                continue
                
            record = {"columns":[], "class":"", "column_size":0, "id":row_id}
            for column_id, column in enumerate(row.split(",")[0:columns_number]):
                record_column = string.strip(column)
                                
                if("?" == record_column):
                    print "WARNING: Cannot handle unknown values in dataset!\n Decision tree will not be correct!"
                
                if(record_column not in self.fields[column_id]["values"] and record_column != "?"):
                    print  record_column + "!=" + str(self.fields[column_id]["values"])
                    raise FieldValueNotValidException
                else:
                    record["column_size"] += 1
                    record["columns"] += [record_column]
            record["class"] = string.strip(row.split(",")[-1])
            
            self.records += [record]
                
    def __str__(self):
        output = []
        for record in self.records:
            output += ["|".join(record["columns"]) + " = " + record["class"]]
        return "\n".join(output)
    
    def load_names_from_data(self, data_file):
        field_values = {}
        for row_id,row in enumerate(data_file):
            if(string.strip(row) == ""):
                continue
                
            for column_id, column_value in enumerate(row.split(",")):
                column_value = string.strip(column_value)
                
                if not column_id in field_values.keys():
                    field_values[column_id] = {}
                    
                if column_value in field_values[column_id].keys():
                    field_values[column_id][column_value] += 1
                else:
                    field_values[column_id][column_value] = 1
                    
        data_file.seek(0) # Go to the begining...
        self.fields = map(lambda x: {"name": "field_" + str(x),"values":field_values[x]}, field_values)
        
        
    def load_names(self, names_file):
        class_data = []
        for index,record in enumerate(names_file):
            if(string.strip(record) == ""): # SKIP EMPTY LINES
                continue
            
            if(record[0] == "|"):   # SKIP COMMENTS!
                continue
            if(len(record.split(":"))<2):  # SKIP CLASSES AND JUNK
                class_data =  map(lambda x: string.strip(x).replace(".",""), record.split(","))
                continue
            
            record_values = string.strip(record.split(":")[1])
            record_values = record_values.replace(".","")
            
            record_values_array = map(lambda x: string.strip(x), record_values.split(","))   
            record_name = string.strip(record.split(":")[0])
            
            if record_values == "continuous":
                raise ContinuousDataSetException
            else:
                self.fields += [{"name":record_name, "values":record_values_array}]
        
        if(class_data != []):
            self.fields += [{"name":"class", "values":class_data}]
        
            
