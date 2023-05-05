import sys
import toml
import pathlib
from document_issue.utils import get_home

#dev
DIR_TESTS = pathlib.Path(__file__).parent
DIR_MODULE = DIR_TESTS.parent

PATH_MFOM = pathlib.Path(__file__).parent
FPTH_REFERENCE_DOCX = PATH_MFOM / 'default_refdocx.docx'
PATH_DEFAULT_CONFIG = PATH_MFOM / 'config.toml'
PATH_USER_CONFIG = pathlib.Path(get_home()) / '.mf_file_utilities' / 'config.toml'

if PATH_USER_CONFIG.is_file():
    PATH_CONFIG = PATH_USER_CONFIG # allows for user override
else:
    PATH_CONFIG = PATH_DEFAULT_CONFIG

def get_config():
    txt = PATH_CONFIG.read_text()
    return toml.loads(txt)['paths']

def get_dirs(config):
    return config['jobsdrive_linux'], \
        config['jobsdrive_linux_relpth'], \
        config['jobsdrive_windows'], \
        config['jobsdrive_windows_dfsnmspace'], \
        config['userdrive_windows'], \
        config['userdrive_linux'], \

config = get_config()
FDIR_LINUXROOT, \
    FDIR_LINUXREL, \
    FDIR_WINDOWSROOT, \
    FDIR_JDRIVE, \
    FDIR_CDRIVE, \
    FDIR_CLINUXMNT = get_dirs(config)

PATH_LINUXROOT = pathlib.PurePosixPath(FDIR_LINUXROOT)
PATH_WINDOWSROOT = pathlib.PureWindowsPath(FDIR_WINDOWSROOT)
PATH_JDRIVE = pathlib.PureWindowsPath(FDIR_JDRIVE)
PATH_LINUXREL = pathlib.PurePosixPath(FDIR_LINUXREL)
PATH_CDRIVE = pathlib.PureWindowsPath(FDIR_CDRIVE)
PATH_CLINUXMNT = pathlib.PurePosixPath(FDIR_CLINUXMNT)

def get_jobs_roots():
    if sys.platform == 'linux':
        return FDIR_LINUXROOT, PATH_LINUXROOT
    else:
        return FDIR_JDRIVE, PATH_JDRIVE
        
def get_c_drive():
    if sys.platform == 'linux':
        return FDIR_CLINUXMNT, PATH_CLINUXMNT
    else:
        return FDIR_CDRIVE, PATH_CDRIVE

FDIR_JOBS_ROOT, PATH_JOBS_ROOT = get_jobs_roots()
FDIR_USER_C, PATH_USER_C = get_c_drive()

FNM_JOB_DATA_INI = 'Jobdata.ini'
FNM_EXAMPLE_JOB = "J5001"

TU_COMMON_PATHS = (PATH_LINUXROOT, PATH_WINDOWSROOT, PATH_JDRIVE, PATH_LINUXREL, PATH_CDRIVE, PATH_CLINUXMNT)

PATH_DISCLAIMER = PATH_MFOM / 'disclaimer.md'
DIR_TEMPLATES = PATH_MFOM / 'templates'
NAME_MD_HEADER_TEMPLATE = 'docheader.md.jinja'
NAME_MD_DISCLAIMER_TEMPLATE = 'disclaimer.md.jinja'
PATH_REFERENCE_DOCX = pathlib.Path(FPTH_REFERENCE_DOCX)
PATH_REL_IMG = pathlib.Path('../images')

DIR_TESTS = PATH_MFOM.parent / 'tests' 
PATH_JOBS_ROOT_MFOM_TEST = DIR_TESTS / 'jobs'

BUTTON_WIDTH_MIN = '41px'
BUTTON_WIDTH_MEDIUM = '90px'
BUTTON_HEIGHT_MIN = '25px'
ROW_WIDTH_MEDIUM = '120px'
ROW_WIDTH_MIN = '60px'

# documentinfo ------------------------------
#  update this with WebApp data
ROLES = ('Design Lead',
'Project Engineer',
'Engineer',
'Project Coordinator',
'Project Administrator',
'Building Performance Modeller', 
'Passivhaus Engineer',
'Sustainability Consultant'
)

if __name__ == "__main__":
    if __debug__:
        print('loaded')