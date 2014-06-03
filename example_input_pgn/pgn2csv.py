#pgn2csv is free software: you can redistribute it
#and/or modify it under the terms of the GNU General Public License
#as published by the Free Software Foundation, either version 3
#of the License, or (at your option) any later version.

#You should have received a copy of the GNU General Public License
#along with pgn2csv.  If not, see <http://www.gnu.org/licenses/>.

#Copyleft 2012 - Author: chefarov@gmail.com

import sys
import os
import argparse

default_dir = os.getcwd()

'''sourceFile: the path of source file (pgn)  --- outputDir: output directory for (csv files)'''
def process_file(sourceFile,  outputDir=default_dir):    
    #Creating the output Directory
    if os.path.exists(outputDir) == False:    #if directory doesn't exist create it
        os.makedirs(outputDir)                       #also creates intermediate directories
    #Opening files
    sourceFileDirs = sourceFile.split('/')    #in case an absolute path is provided
    sourceFileName = sourceFileDirs[-1]     #take the last part of the path which is the file's name
    foutName = outputDir+'/'+sourceFileName[:-3] + "csv"  
    try:
        fin = open(sourceFile,  'r')
        fout = open(foutName,  'w')
        
        #Reading - Writing files
        fout.write('Event, Site, Date, Round, White, Black, Result, WhiteElo, BlackElo, Eco, Moves')
        for line in fin:
            if line[0:6] == '[Event':   #previous line/row/entry/game is over go on (one pgn can contain multiple games)
                fout.write('\n')   
            if line[0] == '[':            #line containing stats : "[Event" also gets in here
                var,  value = line.split(' ',  1)    #split each line to its 1st whitespace (2nd arg means: 1 split only)
                value = value.replace( ',' ,  '' )         #name fields may contain name and lastname seperated by comma (remove it to keep csv fields intact)
                value = value.rstrip( '\r\n' )      #remove newline chars
                fout.write( value[1:-2] + ', ' )          #also remove last two chars : "] and the 1st one : "
            elif line[0].isdigit():                #line containing moves
                a = line.rstrip('\r\n')        #remove newline character and '\r' $MS$ b00l$h1t
                fout.write( a+' ' )              #write all the moves in one cell
        #Closing the files
        fin.close()
        fout.close()
   
    except IOError:
        print "Input file: ", sourceFile, "or output directory: ", outputDir, " does not exist"

'''sourceDir: the path of the directory containing src files --- outputDir: output directory for (csv files)'''
def process_dir(sourceDir=default_dir, outputDir=default_dir):    
    
    for x in os.listdir(sourceDir):
        if x == "csvFiles":
            continue
        path = sourceDir + '/' + x
        if os.path.isdir(path):                  # directory - recursive call
            folderPaths = path.split('/')   # not the folderName yet ... just splitting the path
            folderName = str(folderPaths[-1])
            if folderName == "csvFiles":
                continue
            outDir = outputDir +'/'+ folderName
            process_dir(path, outDir    )       #recursive call to the new path but output Directory is kept to outDir
        elif path[-4:] == '.pgn':         #if we find a pgn file then we call the process_file func
            process_file(path, outputDir)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='usage: >>python -f file or >>python -d directory')    
    parser.add_argument('-f', '--file',  help='give path of the pgn file')
    parser.add_argument('-d', '--directory',  help='give path of the pgn directory(multiple source files)', default=default_dir)
    parser.add_argument('-o', '--outputdir',  help='give path of output directory (default: current directory)',  default=default_dir)
    args = parser.parse_args()
    
    if args.file == None:  #no specific file specified
        outDir = args.outputdir + '/' + 'csvFiles'
        if os.path.exists(outDir) == False:    #if directory doesn't exist create it
            os.mkdir(outDir)
        process_dir(args.directory,  outDir )       #work with directory
    else:
        process_file(args.file,  args.outputdir)    #work with file
        
    print "Conversion completed successfully"
    
