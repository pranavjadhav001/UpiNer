import xlrd
import pandas as pd
from utils import *
#from db_utils import *
from parse_remarks import *

def change_date(date_str):
	date,month,year = date_str.split('/')
	return '-'.join(['20'+year,month,date])

def get_universal_transaction_dict(file_path):
	workbook = xlrd.open_workbook(file_path)
	df = pd.DataFrame(columns=['Date','Transaction Remarks','Reference Number','Value Date','Withdrawal Amount','Deposit Amount','Balance'])
	sheet = workbook.sheet_by_index(0)

	#read table starting from 22th row
	for rx in range(22,sheet.nrows):
	    df.loc[len(df)] = [x.value for x in sheet.row(rx)]
	    if df.iloc[len(df) -1, 4] == "": 
		    df.iloc[len(df) -1, 4] = 0.0
	    if df.iloc[len(df) -1, 5] == "": 
		    df.iloc[len(df) -1, 5] = 0.0

	#drop redundant column cheque no.
	df = df.drop(['Reference Number'],axis=1)
	# df = page_break_merge_statement(df)

		#remove bottom metainfo
	df.drop(df.tail(18).index,
	        inplace = True)

	final_list = []
	for index,row in df.iterrows():
	    raw_doc = row.to_dict()
	    final_list.append({
	        'Date': change_date(raw_doc['Value Date']),
	        'Amount': raw_doc['Withdrawal Amount']+raw_doc['Deposit Amount'],
	        'TransactionType': determine_transaction_type(raw_doc),
	        'Balance':raw_doc['Balance'],
	        'Remarks_parsed':hdfc_remark_parse(raw_doc['Transaction Remarks']),
	        'Remarks_raw':raw_doc['Transaction Remarks'],
	        'source':'hdfc_bank'
	    })
	return final_list

if __name__ == "__main__":
    parser = argparse.ArgumentParser(formatter_class=
    argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--excel_path',help='path to xls',type=str)
    args = parser.parse_args()
    transaction_list = get_universal_transaction_dict(args.excel_path)
    connection = create_connection('global_statement.db')
    create_table_icici_statement('ALL_TRANSACTION', connection)
    insert_many('ALL_TRANSACTION', transaction_list, connection)
    cursor = fetch_data(connection, 'ALL_TRANSACTION')
    for row in cursor.fetchall():
        print(row)

