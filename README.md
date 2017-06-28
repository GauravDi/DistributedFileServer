# DistributedFileServer
*************************************************************************************************************************************************************
AUTHOR:
*************************************************************************************************************************************************************
NAME      : Gaurav Diwate
Occupation: Student at ITP department at University of Colorado Boulder.
SID       : 105755934
IDENTIKEY : gadi5945
Contact   : Email  :  Gaurav.Diwate@coorado.edu
            Phone  :  720-345-1611
************************************************************************************************************************************************************

WELCOME!
                   
DATA COMMUNICATIONS I PROGRAMMINIG ASSIGNMENT 4 TO BUILD DISTRIBUTED FILE SYSTEM FOR RELIABLE AND SECURE FILE STORAGE.

SOFTWARE VERSION :Python 2.7.10

***********************************************************************************************************************************************************
PROGRAMM FEATURES:
***********************************************************************************************************************************************************
     
1. Program builds a distributed file system which handles client requests to save file pieces on different servers and retrieve back. 

2. CLIENT: Client devides a file into four pieces and then puts those pieces on different four servers. Client requests for a list of all files stored
           on servers. Client also requests for file data and reconstructs the original file and saves. 

3. SERVERS: Total four servers are created which accepts file pieces and saves on respective directory folders named by username. Server returns
            stored file list and file pieces upon request from client.  

4. SECURITY:Username and Password Authentication System is implemented so that data remained secured as a user will not get any access to the data of 
            User.    
5. THREADING:Multithreading is implemented to accept multiple client requests at the same time.

6. RELIABILITY: Even if couple of servers are offline, original file can be re-constructed. This is implemented in the program and if not, error message
                is printed.

7. EXTRA CREDIT: TRAFFIC OPTIMIZATION: This is implemented by accepting the data from only two good servers so that the file can be re-constructed successfuly. 
 
***********************************************************************************************************************************************************

