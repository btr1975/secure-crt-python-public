# secure-crt-python-public

## Created By: Benjamin P. Trachtenberg

### Contact Information:  e_ben_75-python@yahoo.com
### If you have any questions e-mail me

### LinkedIn: [Ben Trachtenberg](https://www.linkedin.com/in/ben-trachtenberg-3a78496)
### Docker Hub: [Docker Hub](https://hub.docker.com/r/btr1975)
### Ansible Galaxy: [Ansible Galaxy](https://galaxy.ansible.com/btr1975/)

### About

This script is to be used with SecureCRT by [VanDyke Software](https://forums.vandyke.com)

### External Used Libraries
* diff-match-patch: [Google](https://github.com/google/diff-match-patch)
* xlsxwriter: [John McNamara](https://github.com/jmcnamara/XlsxWriter)
* persistentdatatools [Me](https://github.com/btr1975/persistentdatatools)

### Some instructions

Run the script secure-crt-python.py from the script runner in SecureCRT, use the following commands when logged into
a device.
* #start
* #pre
* #post
* #diffhtml
* #diffxls
* #health

### Current issues

* Nexus systems seem to stall when reading the screen, I am working on figuring that out.