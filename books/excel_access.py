#!/usr/bin/python

import xlrd
import xlwt
import os

class ExcelStatement:
    """ Provides different methods to generate excel statements """
    
    def __init__(self, uploaded_file, policy_nos_from_db):
        self.our_statements_filename = "/tmp/our_statements.xls"
        self.others_statements_filename = "/tmp/others_statements.xls"
        self.source_filename = "/tmp/source_excel_file.xls"
        self.policy_nos_from_db = policy_nos_from_db
        destination = open(self.source_filename, "wb+")
        for chunk in uploaded_file.chunks():
            destination.write(chunk)
        destination.close()
        book = xlrd.open_workbook(self.source_filename)
        self.sheet = book.sheets()[0]
        self.header_row = self.sheet.row_values(0) # list of headings
        self.policy_nos_from_xl = \
                self.sheet.col_values(self._get_header_colnum("Policy Number")) #Getting all policy numbers
        # deleting the temp source file
        try:
            os.remove(self.source_filename)
        except:
            pass

    def _get_header_colnum(self, heading):
    	"""Returns the column number of given header"""
    	for (colnum, col) in enumerate(self.header_row):
    		if col == heading:
    			return colnum
    
    def _write_row(self, values, given_sheet, rownum=0):
    	"""Writes the given list of values to given row in the given sheet"""
    	for (colnum, value) in enumerate(values):
    		given_sheet.write(rownum,colnum,value)
    
    def generate_statements(self):
        """ Generating the filtered excel statements """
        others_workbook = xlwt.Workbook()
        others_sheet = others_workbook.add_sheet("Sheet1")
        self._write_row(self.header_row, others_sheet) # Copying the headings
        others_rownum = 1
        
        our_workbook = xlwt.Workbook()
        our_sheet = our_workbook.add_sheet("Sheet1")
        self._write_row(self.header_row, our_sheet) # Copying the headings
        our_rownum = 1
        
        for rownum in xrange(1, self.sheet.nrows):
        	if self.policy_nos_from_xl[rownum] in self.policy_nos_from_db:
                # Populating our_statements excel sheet
        		self._write_row(self.sheet.row_values(rownum),our_sheet,our_rownum)
        		our_rownum += 1
        	else:
                # Populating others statements excel sheet
        		self._write_row(self.sheet.row_values(rownum),others_sheet,others_rownum)
        		others_rownum += 1
        # Saving the created excel sheets
        #others_workbook.save(self.others_statements_filename)
        #our_workbook.save(self.our_statements_filename)

        # creating correspoding file objects
        #others_file_obj = open(self.others_statements_filename)
        #our_file_obj = open(self.our_statements_filename) 

        # trying to delete temp files
        #try:
        #    os.remove(self.our_statements_filename)
        #    os.remove(self.others_statements_filename)
        #except:
        #    pass

        return our_workbook, others_workbook

    def get_unknown_policynums(self):
       """ Returns the policy_nos in database that are not in excel sheet """
       error_list = []
       for num in self.policy_nos_from_db:
           if num not in self.policy_nos_from_xl:
               error_list.append(num)
       return error_list

    def get_values_with_policynum(self, policy_number):
        "Returns the row with the given policy number"
        for (rownum, row_content) in enumerate(self.policy_nos_from_xl):
            if row_content == policy_number:
                return self.sheet.row_values(rownum)

        


