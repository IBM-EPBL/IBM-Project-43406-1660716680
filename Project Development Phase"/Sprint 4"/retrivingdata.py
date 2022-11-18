import ibm_db

import ibm_db.connection("DATABASE=bludb;HOSTNAME=824dfd4d-99de-440d-9991-629c01b3832d.bs2io90l08kqb1od8lcg.databases.appdomain.cloud;PORT=30119;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=zyh74291;PWD=zAF3WthDCswTE4gC",'','')
print(conn)
print("connection successful...")

sql = "SELECT * FROM Registration"
stmt =ibm_db.exec-immediate(conn, sql)
dictionary = ibm_db.fetch_both(stmt)
while dictionary != False:
    #print(dictionary)
    print("The Name is : ", dictionary)
    #print("The Username is :",dictionary["USRENAME"])
    #print("The Password is :",dictionary["PASSWORD"])
    #print("The Confirm Password is :",dictionary["CONFIRM PASSWORD"])
    #print("The Gender is :",dictionary["GENDER"])    
    #print("The Email is :",dictionary["EMAIL"])
    #print("The Phone Number is :",dictionary["PHONE NUMBER"])
    print("************************")
    dictionary = ibm_db.fetch_both_(stmt)

    