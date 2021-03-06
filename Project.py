# -*- coding: utf-8 -*-

########### GUI2Exe SVN repository information ###################
# $Date$
# $Author$
# $Revision$
# $URL$
# $Id$
########### GUI2Exe SVN repository information ###################

# Start the imports

import sys
import os
import time

from Utilities import odict, now


class Project(odict):
    """
    A class derived from an ordered dictionary which holds all the information
    about GUI2Exe projects, for all the compilers available.
    """

    def __init__(self, configuration=None, name=""):
        """
        Default class constructor.

        
        **Parameters:**

        * configuration: the project data;
        * name: the project name as entered by the user.
        """        

        # Initialize the ordered dictionary
        # "Project" is a dictionary of dictionaries: the top level keys specify
        # which compiler the children keys refer to (i.e., py2exe, py2app etc...)
        # and for every top level key the secondary dictionary contains the
        # project configuration as entered by the user
        odict.__init__(self, configuration)

        # Store the data we are going to need later        
        self.name = name
        self.creationDate = time.localtime(time.time())
        self.customCode = {}
        self.postCompile = {}
        self.hasBeenCompiled = False
        self.missingModules = []
        self.binaryDependencies = []
        self.buildOutputs = {}
        self.useUPX = {}
        self.buildInno = {}
        self.extraKeywords = {}


    def Update(self, compiler, keyName, keyValue):
        """
        Updates the project with data inserted by the user.

        
        **Parameters:**

        * compiler: the selected executable-builder;
        * keyName: the option name for the selecte compiler;
        * keyValue: the option value for the selecte compiler.
        """

        self[compiler][keyName] = keyValue
                

    def SetConfiguration(self, compiler, configuration):
        """
        Sets a whole configuration for the selected compiler.

        
        **Parameters:**

        * compiler: the selected executable-builder;
        * configuration: the project configuration to save.
        """

        self[compiler] = configuration


    def GetConfiguration(self, compiler):
        """
        Returns the configuration for the selected compiler.

        
        **Parameters:**

        * compiler: the selected executable-builder.
        """

        return self[compiler]


    def SetName(self, name):
        """
        Sets the project name.

        
        **Parameters:**

        * name: the project name given by the user.
        """

        self.name = name
        

    def GetName(self):
        """ Returns the project name. """

        return self.name


    def GetCreationDate(self):
        """ Returns the project creation date. """

        if type(self.creationDate) == time.struct_time:
            return time.strftime("%d %B %Y @ %H:%M:%S", self.creationDate)
        
        return self.creationDate
    

    def SetCustomCode(self, compiler, code):
        """
        Sets the custom code entered by the user.

        
        **Parameters:**

        * compiler: the compiler to which the custom code applies;
        * code: the custom code entered by the user.
        """

        if isinstance(self.customCode, basestring):
            # Coming from the old database syntax
            self.customCode = {}
            
        self.customCode[compiler] = code

        
    def GetCustomCode(self, compiler):
        """
        Returns the custom code entered by the user.

        
        **Parameters:**

        * compiler: the compiler to which the custom code applies.
        """

        if isinstance(self.customCode, basestring):
            # Old database syntax
            tmp = self.customCode[:]
            self.customCode = {}
            self.customCode[compiler] = tmp

        if compiler not in self.customCode:
            # No custom code for this compiler
            return ""

        return self.customCode[compiler]


    def SetPostCompileCode(self, compiler, code):
        """
        Sets some custom post-compilation code to be executed.

        
        **Parameters:**

        * compiler: the compiler to which the post-compilation code applies;
        * code: the post-compilation code entered by the user.
        """

        if not hasattr(self, "postCompile"):
            # Old database syntax
            self.postCompile = {}
            
        self.postCompile[compiler] = code
        

    def GetPostCompileCode(self, compiler):
        """
        Returns the custom post-compilation code to be executed (if any).

        
        **Parameters:**

        * compiler: the compiler to which the post-compilation code applies.
        """

        if not hasattr(self, "postCompile"):
            # Old database syntax
            self.postCompile = {}
            
        if compiler not in self.postCompile:
            # No post-compilation code for this compiler
            return ""
        
        return self.postCompile[compiler]


    def SetCompilationData(self, missingModules, binaryDependencies):
        """
        Sets the results of the compilation process, in terms of what the compiler
        says are the binary dependencies (dlls) and the missing modules (Python files).
        This method applies only to py2exe compiled scripts.
        
        
        **Parameters:**

        * missingModules: the modules py2exe thinks are missing;
        * binaryDependencies: the dlls py2exe suggests you to include in your distribution.
        """

        self.missingModules = missingModules
        self.binaryDependencies = binaryDependencies


    def GetCompilationData(self):
        """ Returns the result of the compilation process. """

        return self.missingModules, self.binaryDependencies


    def HasBeenCompiled(self):
        """ Checks if a project has been compiled or not. """

        return self.hasBeenCompiled


    def GetUseUPX(self, compiler):
        """
        Returns if the user wants to use UPX compression based on the chosen compiler.

        
        **Parameters:**

        * compiler: the compiler for which we want to use UPX compression.
        """
        
        if not hasattr(self, "useUPX"):
            # Old database syntax
            self.useUPX = {}
            
        if compiler not in self.useUPX:
            # No UPX compression for this compiler
            return False

        return self.useUPX[compiler]


    def SetUseUPX(self, compiler, use):
        """
        Sets whether the user wants to use UPX compression based on the chosen compiler.

        
        **Parameters:**

        * compiler: the compiler for which we want to use UPX compression;
        * use: whether to use UPX compression or not.
        """
        
        if not hasattr(self, "useUPX"):
            # Old database syntax
            self.useUPX = {}
            
        self.useUPX[compiler] = use


    def GetBuildInno(self, compiler):
        """
        Returns if the user wants to build a Inno Setup script based on the chosen compiler.

        
        **Parameters:**

        * compiler: the compiler for which we want to build an Inno Setup script.
        """
        
        if not hasattr(self, "buildInno"):
            # Old database syntax
            self.buildInno = {}
            
        if compiler not in self.buildInno:
            # No Inno Setup script for this compiler
            return False
        
        return self.buildInno[compiler]


    def SetBuildInno(self, compiler, build):
        """
        Sets whether the user wants to build an Inno Setup script based on the chosen compiler.

        
        **Parameters:**

        * compiler: the compiler for which we want to build an Inno Setup script;
        * use: whether to build the script or not.
        """
        
        if not hasattr(self, "buildInno"):
            # Old database syntax
            self.buildInno = {}
            
        self.buildInno[compiler] = build


    def GetExtraKeywords(self, compiler, exeIndex):
        """
        Returns the extra keywords chosen by the user for the target class (py2exe only).

        
        **Parameters:**

        * compiler: the compiler for which we want to get extra keywords;
        * exeIndex: the index of the executable in the list control.
        """
        
        if not hasattr(self, "extraKeywords"):
            # Old database syntax
            self.extraKeywords = {}
            
        if compiler not in self.extraKeywords:
            # No extra keywords for this compiler
            return {}

        if exeIndex not in self.extraKeywords[compiler]:
            return {}
        
        return self.extraKeywords[compiler][exeIndex]


    def SetExtraKeywords(self, compiler, exeIndex, keys):
        """
        Sets the extra keywords chosen by the user for the target class (py2exe only).

        
        **Parameters:**

        * compiler: the compiler for which we want to add the extra keywords;
        * exeIndex: the index of the executable in the list control;
        * keys: a dictionary of keyword-value pairs.
        """
        
        if not hasattr(self, "extraKeywords"):
            # Old database syntax
            self.extraKeywords = {}
            
        self.extraKeywords[compiler] = {exeIndex: keys}


    def RemoveExtraKeywords(self, compiler, exeIndex):
        """
        Removes the extra keywords chosen by the user for the target class (py2exe only).
        
        **Parameters:**

        * compiler: the compiler for which we want to remove the extra keywords;
        * exeIndex: the index of the executable in the list control.
        """

        if not hasattr(self, "extraKeywords"):
            # Old database syntax
            return

        if compiler not in self.extraKeywords:
            # No extra keywords for this compiler
            return 

        if exeIndex not in self.extraKeywords[compiler]:
            return 
        
        self.extraKeywords[compiler].pop(exeIndex)
        
    
    def GetExecutableName(self, compiler):
        """
        Returns the executable name based on the chosen compiler.

        
        **Parameters:**

        * compiler: the compiler for which we want the executable name.
        """

        distDir = True
        extension = (sys.platform == "win32" and [".exe"] or [""])[0]
        configuration = self[compiler]
        # The executable name, for py2exe at least, lives in the folder:
        # /MainPythonFileFolder/dist_directory/
        if compiler in ["py2exe", "cx_Freeze"]:
            script, exename = configuration["multipleexe"][0][1:3]
            if exename.strip():
                script = os.path.normpath(os.path.split(script)[0] + "/" + exename)
            distChoice = configuration["dist_dir_choice"]
            dist_dir = configuration["dist_dir"]
            if not distChoice or not dist_dir.strip():
                # Invalid or not selected distribution folder
                distDir = False
                script = os.path.normpath(os.path.split(script)[0] + "/dist/" + exename)
                
        elif compiler == "PyInstaller":
            # This is not 100% guaranteed to succeed...
            script = configuration["scripts"][-1]
            exename = configuration["exename"]
            dist_dir = configuration["dist_dir"]
            if exename.strip():
                script = os.path.normpath(os.path.split(script)[0] + "/" + exename)
            if configuration["onefile"]:
                distDir = False
            else:
                if not dist_dir.strip():
                    distDir = False

        elif compiler == "py2app":
            script = configuration["script"]
            extension = configuration["extension"]
            if "dist_dir_choice" in configuration:
                distChoice = configuration["dist_dir_choice"]
            else:
                distChoice = False
            dist_dir = configuration["dist_dir"]
            if not distChoice or not dist_dir.strip():
                # Invalid or not selected distribution folder
                distDir = False

        elif compiler == "vendorid":
            script = configuration["script"]
            exename = configuration["exename"]
            distDir = True
            if "build_dir_choice" in configuration:
                distChoice = configuration["build_dir_choice"]
            else:
                distChoice = False
            dist_dir = configuration["build_dir"]
            if not distChoice or not dist_dir.strip():
                # Invalid or not selected distribution folder
                buildDir, name = os.path.split(script)
                dist_dir = "/build_%s"%os.path.splitext(name)[0]
            
        else:
            # Check if the distribution folder is valid
            script = configuration["multipleexe"][0][1]
            distChoice = configuration["dist_dir_choice"]
            dist_dir = configuration["dist_dir"]
            if not distChoice or not dist_dir.strip():
                # Invalid or not selected distribution folder
                distDir = False
                script = os.path.normpath(os.path.split(script)[0] + "/dist/" + exename)
                
            distChoice = configuration["dist_dir_choice"]
            dist_dir = configuration["dist_dir"]
            dist_dir = ((distChoice and dist_dir.strip()) and [dist_dir.strip()] or ["dist"])[0]
                
        if distDir:
            # Distribution folder selected and with a valid name
            path, script = os.path.split(script)
            script = os.path.splitext(script)[0] + extension
            exePath = os.path.normpath(path + "/" + dist_dir + "/" + script)
        else:
            # Distribution folder invalid or not selected
            exePath = script + extension

        if extension:
            if exePath.count(extension) > 1:
                exePath = exePath[0:-len(extension)]
                
        return os.path.normpath(exePath)


    def GetManifestFileName(self, compiler):
        """
        Returns the manifest file name for Windows XP executables.

        
        **Parameters:**

        * compiler: the compiler for which we build the manifest file.
        """

        configuration = self[compiler]
        if "create_manifest_file" not in configuration:
            # No such thing for py2exe, py2app
            return

        addManifest = configuration["create_manifest_file"]
        if not bool(int(addManifest)):
            # User has not requested it
            return

        extension = ".exe.manifest"
        programName = None

        if compiler == "cx_Freeze":

            script, target = configuration["multipleexe"][0][1:3]
            dist_dir = configuration["dist_dir"]
            dist_choice = configuration["dist_dir_choice"]

            dirName, fileName = os.path.split(script)
            fileNoExt, ext = os.path.splitext(script)
            singleFileNoExt = os.path.split(fileNoExt)[1]
            
            if not target.strip():
                # Invalid target name or executable not renamed
                programName = singleFileNoExt
                if not dist_dir.strip() or not dist_choice:
                    # Invalid distribution folder or not selected
                    manifest = fileNoExt + extension
                else:
                    manifest = os.path.normpath(dirName + "/" + dist_dir + "/" + singleFileNoExt + extension)
            else:
                # Executable has been renamed inside GUI2Exe
                programName = target.replace(".exe", "").strip()
                if not dist_dir.strip() or not dist_choice:
                    # Invalid distribution folder or not selected
                    manifest = os.path.normpath(dirName + "/dist/" + target.strip() + extension[4:])
                else:
                    # User has changed the name of the distribution directory
                    manifest = os.path.normpath(dirName + "/" + dist_dir + "/" + target.strip() + extension[4:])

        elif compiler == "PyInstaller":
            script, dist_dir, target = configuration["scripts"][-1], configuration["dist_dir"], \
                                       configuration["exename"]
            onefile = configuration["onefile"]
            dirName, fileName = os.path.split(script)
            fileNoExt, ext = os.path.splitext(script)
            singleFileNoExt = os.path.split(fileNoExt)[1]
            if onefile:
                # Distribution is singlefile for PyInstaller
                programName = target.replace(".exe", "")
                manifest = os.path.normpath(dirName + "/" + target.replace(".exe", "") + extension)
            else:
                # Distribution is singledir for PyInstaller
                programName = singleFileNoExt
                manifest = os.path.normpath(dirName + "/" + dist_dir + "/" + singleFileNoExt + extension)
                
        else:
            # bbFreeze compiler
            script, dist_dir, dist_choice = configuration["multipleexe"][0][1], configuration["dist_dir"], \
                                            configuration["dist_dir_choice"]
            dirName, fileName = os.path.split(script)
            fileNoExt, ext = os.path.splitext(script)
            singleFileNoExt = os.path.split(fileNoExt)[1]
            if dist_dir.strip() or not dist_choice:
                # Invalid distribution folder or not selected
                manifest = os.path.normpath(dirName + "/" + dist_dir + "/" + singleFileNoExt + extension)
            else:
                # User has changed the name of the distribution directory
                manifest = os.path.normpath(dirName + "/dist/" + singleFileNoExt + extension)
            programName = singleFileNoExt
            
        return manifest, programName


    def AssignBuildOutput(self, compiler, outputText):
        """
        Assigns the full build output text to the project for later viewing.

        
        **Parameters:**

        * compiler: the compiler used to build the executable;
        * outputText: the full build output text from the compiler.
        """

        if not hasattr(self, "buildOutputs"):
            # Old database syntax
            self.buildOutputs = {}

        # Add time information to the build output text (at the top)
        outputText = now() + "/-/-/\n" + outputText
        self.buildOutputs[compiler] = outputText


    def GetBuildOutput(self, compiler):
        """
        Retrieves the full build output text (if any).

        
        **Parameters:**

        * compiler: the compiler used to build the executable;
        """
        
        if not hasattr(self, "buildOutputs"):
            # Old database syntax
            self.buildOutputs = {}
            return ""

        if compiler not in self.buildOutputs:
            # This compiler has not been used yet
            return ""
        
        return self.buildOutputs[compiler]

    
    def GetDistDir(self, compiler):
        """
        Retrieves the distribution directory for the specific compiler.

        
        **Parameters:**

        * compiler: the compiler used to build the executable;
        """

        exeName = self.GetExecutableName(compiler)
        return os.path.split(exeName)[0]

    