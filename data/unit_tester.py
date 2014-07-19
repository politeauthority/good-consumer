#!/usr/bin/python
"""
  UNIT TESTER
"""

import sys
sys.path.append( '../web/' )
import MVC as MVC

MVC               = MVC.MVC()
JobLog            = MVC.loadModel('JobLog')
ModelCompany      = MVC.loadModel('Company')
ModelCompanies    = MVC.loadModel('Companies')
ModelCompanyTypes = MVC.loadModel('CompanyTypes')
ModelNews         = MVC.loadModel('News')
ModelNewsSources  = MVC.loadModel('NewsSources')
ModelPerson       = MVC.loadModel('Person')
Wikipedia         = MVC.loadDriver('Wikipedia')
GoogleNews        = MVC.loadDriver('GoogleNews')

Debugger          = MVC.loadHelper('Debug')

if __name__ == "__main__":
  ModelNewsSources.updateCounts()