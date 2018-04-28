# EIGRP Q-Count
Queue Count(Q Cnt) is the number of EIGRP packets (Update, Query or Reply) in the queue that are awaiting transmission. Ideally, you want this number to be "0" otherwise it might be an indication of congestion on the network!!                    
 
 This App aimed to extract the Q Count for each EIGRP neighbour by connecting to each router via SSH (Paramiko) then execute the "Show ip eigrp neighbors" and analyze its output, consequently depicts the results in a convenient way!!                                           
 
 
 Please share your experience and thoughts!!!!                 
