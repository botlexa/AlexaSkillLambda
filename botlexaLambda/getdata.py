#!/usr/bin/python
import sys
import logging
import psycopg2
import json

from db_util import make_conn, fetch_one_row_data, fetch_data, fetch_custom_data, execute_query, execute_query_value
def getcustomername(custid):
    conn = make_conn()
    query_cmd = "select Name from UserMaster where UserID = " + str(custid) + ';'
    result = fetch_one_row_data(conn, query_cmd)
    conn.close() 
    return result
def getformdata(formid):
    conn = make_conn()

    query_cmd = "select FieldMaster.FieldName, FieldDetails.FieldValue from FieldDetails " \
                "INNER JOIN FieldMaster ON FieldMaster.FieldMasterID = FieldDetails.FieldMasterID " \
                "WHERE FieldDetails.TemplateCustomerMappingID = " + str(formid) + ";"
    # query_cmd = "select FieldMaster.FieldName, FieldDetails.FieldValue from FieldDetails INNER JOIN FieldMaster ON FieldMaster.FieldMasterID = FieldDetails.FieldMasterID WHERE FieldDetails.TemplateCustomerMappingID = 14;"
    result = fetch_data(conn, query_cmd)
    conn.close()
    return result
def getformNumber(formnumber):
    conn = make_conn()
    TemplateCustomerMappingID = ''

    query_cmd = "INSERT INTO TemplateCustomerMapping(UniqueFormNumber, TemplateMasterID) " \
                "VALUES(0, " + str(formnumber) + ") RETURNING TemplateCustomerMappingID"
    # query_cmd = "INSERT INTO TemplateCustomerMapping (UniqueFormNumber, TemplateMasterID) VALUES(0, 1) RETURNING TemplateCustomerMappingID "
    TemplateCustomerMappingID = execute_query_value(conn, query_cmd)

    query_cmd = "INSERT INTO FieldDetails(FieldValue, FieldMasterID, TemplateCustomerMappingID) " \
                "SELECT '', FieldMasterID, " + str(TemplateCustomerMappingID) + \
                " from FieldMaster WHERE TemplateMasterID = " + str(formnumber) + ";"
    # query_cmd = "INSERT INTO FieldDetails(FieldValue, FieldMasterID, TemplateCustomerMappingID) SELECT '', FieldMasterID, " + str(TemplateCustomerMappingID) + " from FieldMaster WHERE TemplateMasterID = 1;"
    result = execute_query(conn, query_cmd)
    conn.close()
    return TemplateCustomerMappingID

def getformfields(formnumber):
    conn = make_conn()
    query_cmd = "select FieldMasterID, FieldName from FieldMaster where TemplateMasterID" \
                " = " + str(formnumber) + ";"
    # query_cmd = "select FieldMasterID, FieldName from FieldMaster where TemplateMasterID = 1;"
    result = fetch_data(conn, query_cmd)

    conn.close()
    return result

def getformname(custid):
    conn = make_conn()
    query_cmd = "select TemplateName, TemplateMasterID  from TemplateMaster where UserID = " \
                "" + str(custid) + ';'
    result = fetch_data(conn, query_cmd)
    conn.close()
    return result
def saveformfields(formid, fieldid, value):
    conn = make_conn()
    #query_cmd = "UPDATE FieldDetails SET FieldValue = 'PANKAJ' WHERE FieldMasterID = 1 AND TemplateCustomerMappingID = 14"
    query_cmd = "UPDATE FieldDetails SET FieldValue = '" + str(value) + "' WHERE " \
                "FieldMasterID = " + strr(fieldid) + " AND TemplateCustomerMappingID = " + str(formid)
    execute_query(conn, query_cmd)
    conn.close()
    return "OK"