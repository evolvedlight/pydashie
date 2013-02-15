import os

import logging
import shutil
import subprocess
from scss import Scss

log = logging.getLogger('PydashieCompiler')
logging.basicConfig()
log.setLevel(logging.INFO)
#Requirements:

#pip install pyScss


#
def main():
    #Options
    refreshDashingCode=True
    
    
    #Check out dashing into temp directory
    current_directory = os.getcwd()
    
    tmp_dir = os.path.join(current_directory, 'tmp')
    if not os.path.exists(tmp_dir):
        log.info('Creating tmp dir %s' % tmp_dir)
        os.mkdir(tmp_dir)
        
    tmp_build_dir = os.path.join(tmp_dir, 'bin')
    if not os.path.exists(tmp_build_dir):
        log.info('Creating bin dir %s' % tmp_build_dir)
        os.mkdir(tmp_build_dir)
    
    dashing_dir = os.path.join(current_directory, 'tmp', 'dashing')
    if refreshDashingCode:
        if os.path.exists(dashing_dir):
            log.info('Removing old Dashing Clone')
            shutil.rmtree(dashing_dir)
            
        log.info('Creating dashing tmp dir %s' % dashing_dir)
        os.mkdir(dashing_dir)
    
    os.chdir(dashing_dir)
    if refreshDashingCode:
        log.info('Cloning Dashing Code')
        subprocess.call("git clone https://github.com/Shopify/dashing", shell=True)
    fileList = []
    for root, subFolders, files in os.walk(dashing_dir):
        for fileName in files:
            if 'scss' in fileName: 
                fileList.append(os.path.join(root, fileName))
                log.info('Found SCSS to compile: %s' % fileName)
    import StringIO
    css_output = StringIO.StringIO()
    css = Scss()
    css_output.write('\n'.join([css.compile(open(filePath).read()) for filePath in fileList]))
    
    fileList = []
    for root, subFolders, files in os.walk(dashing_dir):
        for fileName in files:
            if 'css' in fileName and 'scss' not in fileName: 
                fileList.append(os.path.join(root, fileName))
                log.info('Found CSS to append: %s' % fileName)
    css_output.write('\n'.join([open(filePath).read() for filePath in fileList]))
    
    with open(os.path.join(tmp_build_dir, 'application.css'), 'w') as outfile:
        outfile.write(css_output.getvalue())
        log.info('Wrote CSS out')

if __name__ == '__main__':
    main()