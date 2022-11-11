import pandas as pd
from s3ops import GetS3File

tryagain= True
def getFile(filename,aws_key,aws_secret,bucket):
	counter = 0
	success=False
	while counter<3:
		try:
			dfFile = GetS3File(filename,aws_key,aws_secret,bucket)
			
			counter = 3
			dfFile = dfFile.set_index('sourceID')
			success=True
		except:
			counter+=1
	if not(success):
		dfFile = pd.DataFrame(columns = ['sourceID','translation'],dtype=str)
		dfFile = dfFile.set_index('sourceID')
	return(dfFile)




