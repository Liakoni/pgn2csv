#pgn2csv is free software: you can redistribute it
#and/or modify it under the terms of the GNU General Public License
#as published by the Free Software Foundation, either version 3
#of the License, or (at your option) any later version.

#You should have received a copy of the GNU General Public License
#along with pgn2csv.  If not, see <http://www.gnu.org/licenses/>.

#Copyleft 2012 - Author: chefarov@gmail.com
#version 1.1

import sys
import os
import argparse
from collections import OrderedDict

default_dir = os.getcwd()

'''process pgn's lines, seperating tag's from their values and removing characters like quotes commas etc'''
def process_line(line, tags):
    tag,  value = line.split(' ',  1)            #split each line to its 1st whitespace (2nd arg means: 1 split only)             
    tag = tag[1:]                                        #remove '[' (1st character)
    value = value.replace( ',' ,  '' )       #name fields may contain name and lastname seperated by comma (remove it to keep csv fields intact)
    value = value.rstrip( '\r\n' )             #remove newline chars
    if tags.has_key(tag):                           #do not add arbitrary tags
        tags[tag] = value[1:-2]                   #also remove last two chars : "] and the 1st one : "

def write_to_file(tags, fout):
    global id
    for v in tags.values():
        fout.write(str(v)+', ') 
    
def initDic(dict):
    for key in dict.keys():
        dict[key] = ' '

'''sourceFile: the path of source file (pgn)  --- outputDir: output directory for (csv files)'''
def process_file(sourceFile,  outputDir=default_dir): 
    print 'proc file .... ', sourceFile   
    global id
    #Creating the output Directory
    if os.path.exists(outputDir) == False:    #if directory doesn't exist create it
        os.makedirs(outputDir)                #also creates intermediate directories
    #Opening files
    sourceFileDirs = sourceFile.split('/')  #in case an absolute path is provided
    sourceFileName = sourceFileDirs[-1]     #take the last part of the path which is the file's name
    foutName = os.path.join(outputDir,sourceFileName)  
    print foutName
    try:
        fin = open(sourceFile, 'r')
        fout = open(foutName,  'w')

        #Reading - Writing files
        fout.write('Id, Event, Site, Date, Round, White, Black, Result, ECO, WhiteTitle, WhiteElo, WhiteFideId, '+ 
                          'BlackTitle, BlackElo, BlackFideId, EventDate, Opening, Variation, Title, Moves')
        initItems = [('Id', ' '), ('Event',' '), ('Site',' '), ('Date',' '), ('Round',' '), ('White',' ') , ('Black',' '), 
                           ('Result',' '), ('ECO',' '),  ('WhiteTitle', ' '), ('WhiteElo', ' ') , ('WhiteFideId',' '),  ('BlackTitle', ' '), 
                           ('BlackElo',' '), ('BlackFideId',' ') , ('EventDate', ' '),  ('Opening', ' '), ('Variation',' ')]
        tags = OrderedDict(initItems)         #ordered Dictionary creation
    
        flag = True                           #helping flag to apply [pgn] , [/pgn] pgn4web flags only once for every game in moves section
        firstLineFlag = True              #helping flag to not apply /pgn tag in 1st line

        for line in fin:
            if line[0:7] == '[Event ':       #previous line/row/entry/game is over go on (one pgn can contain multiple games)
               #reaching here means line contains event info
                if firstLineFlag == False:         #every time we come up with a new game except the 1st time
                    fout.write(' [/pgn]')         #close the pgn4web tag
                firstLineFlag = False
                flag = True
                initDic(tags)                            #empty dictionary from previous game's values
                tags['Id'] = id
                id = id + 1
                fout.write('\n') 
                process_line(line, tags)           #now we are ready to write the tag's value like we do in every tag
            elif line[0].isdigit():                               #moves section
             
                write_to_file(tags, fout)       #move the tags' values from dictionary to file before writing moves 
                 #before the moves append the white-black info (not in the tags) - feature helping drupal site :P
                fout.write(tags['White']+' - '+tags['Black']+', ')
                
                while line not in ['\n', '\r\n'] :     #read all the lines containing moves
                    if flag:                                        #apply tag only before 1st move in each game
                        fout.write('[pgn] ')             #apply tags for pgn4web automation board presentation software
                        flag = False                            #do not apply tag after every newline(from pgn file) with moves
                    a = line.rstrip('\r\n')        #remove newline character and '\r' $MS$ b00l$h1t
                    fout.write( a+' ' )              #write all the moves in one cell
                    line = fin.next()                  #read next line
                    if len(line) == 0:                 #trying to catch EOF but never yet - StopIteration exception is raised and handled below
                        break
            elif len(line) > 2 :                      #not empty remember \r\n make len(line) == 2 
                process_line(line, tags)          #ordinary tag, write its value to dictionary(tags) 
        #end of external for loop
            
        fout.write('[/pgn]')                   #last tag outside the loop
        #Closing the files
        fin.close()
        fout.close()
    except StopIteration:
        fout.write('[/pgn]')        #because when there is not an empty line at the End Of File we get that exception in line 76: line=fin.next()
        fout.close()
        fin.close()
    except IOError:
        print "Sth wrong with Input file: ", sourceFile, " or output directory: ", outputDir
        fout.close()
        fin.close()

'''sourceDir: the path of the directory containing src files --- outputDir: output directory for (csv files)'''
def process_dir(sourceDir=default_dir, outputDir=default_dir):    

    for x in os.listdir(sourceDir):
        if x == "csvFiles":
            continue
        path = os.path.join(sourceDir, x)
        if os.path.isdir(path):                  # directory - recursive call
            if '/' in path:
                folderPaths = path.split('/')   # not the folderName yet ... just splitting the path
            else:
                folderPaths = path.split('/')   # not the folderName yet ... just splitting the path
                
            folderName = str(folderPaths[-1])
            if folderName == "csvFiles":
                continue
            outDir = os.path.join(outputDir, folderName)
            process_dir(path, outDir    )       #recursive call to the new path but output Directory is kept to outDir
        elif path[-4:] == '.pgn':         #if we find a pgn file then we call the process_file func
            process_file(path, outputDir)


if __name__ == "__main__":
    global id             #counter for the 1st column of csv
    parser = argparse.ArgumentParser(description='usage: >>python -f file or >>python -d directory')    
    parser.add_argument('-f', '--file',  help='path of the pgn file')
    parser.add_argument('-d', '--directory',  help='path of the pgn directory(multiple source files)-(default: current directory', default=default_dir)
    parser.add_argument('-o', '--outputdir',  help='path of output directory (default: current directory)',  default=default_dir)
    parser.add_argument('-i', '--id',  help='starting id counter (default = 1)',  default=1)
    args = parser.parse_args()
    
    id = int(args.id)
    if args.file == None:  #no specific file specified
        outDir = os.path.join(args.outputdir, 'csvFiles')
        if os.path.exists(outDir) == False:    #if directory doesn't exist create it
            os.mkdir(outDir)
        process_dir(args.directory,  outDir )       #work with directory
    else:
        process_file(args.file,  args.outputdir)    #work with file

    print "Conversion completed successfully"

