#!/bin/bash
PROJECT_NAME="MacCleanerPro"

# Créer la structure de base
mkdir -p "$PROJECT_NAME"
mkdir -p "$PROJECT_NAME.xcodeproj"

# Créer le fichier de projet Xcode minimal mais fonctionnel
cat > "$PROJECT_NAME.xcodeproj/project.pbxproj" << 'PBXEOF'
// !$*UTF8*$!
{
	archiveVersion = 1;
	classes = {};
	objectVersion = 56;
	objects = {
		B8E1A1001 /* MacCleanerProApp.swift */ = {
			isa = PBXFileReference;
			lastKnownFileType = sourcecode.swift;
			path = MacCleanerProApp.swift;
			sourceTree = "<group>";
		};
		B8E1A1002 /* ContentView.swift */ = {
			isa = PBXFileReference;
			lastKnownFileType = sourcecode.swift;
			path = ContentView.swift;
			sourceTree = "<group>";
		};
		B8E1A1003 /* MacCleanerPro.app */ = {
			isa = PBXFileReference;
			explicitFileType = wrapper.application;
			includeInIndex = 0;
			path = MacCleanerPro.app;
			sourceTree = BUILT_PRODUCTS_DIR;
		};
		B8E1A1004 /* Sources */ = {
			isa = PBXSourcesBuildPhase;
			buildActionMask = 2147483647;
			files = (
				B8E1A1011 /* MacCleanerProApp.swift in Sources */,
				B8E1A1012 /* ContentView.swift in Sources */,
			);
			runOnlyForDeploymentPostprocessing = 0;
		};
		B8E1A1005 /* Frameworks */ = {
			isa = PBXFrameworksBuildPhase;
			buildActionMask = 2147483647;
			files = ();
			runOnlyForDeploymentPostprocessing = 0;
		};
		B8E1A1006 /* Resources */ = {
			isa = PBXResourcesBuildPhase;
			buildActionMask = 2147483647;
			files = ();
			runOnlyForDeploymentPostprocessing = 0;
		};
		B8E1A1007 /* MacCleanerPro */ = {
			isa = PBXGroup;
			children = (
				B8E1A1001 /* MacCleanerProApp.swift */,
				B8E1A1002 /* ContentView.swift */,
			);
			path = MacCleanerPro;
			sourceTree = "<group>";
		};
		B8E1A1008 /* Products */ = {
			isa = PBXGroup;
			children = (
				B8E1A1003 /* MacCleanerPro.app */,
			);
			name = Products;
			sourceTree = "<group>";
		};
		B8E1A1009 = {
			isa = PBXGroup;
			children = (
				B8E1A1007 /* MacCleanerPro */,
				B8E1A1008 /* Products */,
			);
			sourceTree = "<group>";
		};
		B8E1A1010 /* MacCleanerPro */ = {
			isa = PBXNativeTarget;
			buildConfigurationList = B8E1A1020 /* Build configuration list for PBXNativeTarget "MacCleanerPro" */;
			buildPhases = (
				B8E1A1004 /* Sources */,
				B8E1A1005 /* Frameworks */,
				B8E1A1006 /* Resources */,
			);
			buildRules = ();
			dependencies = ();
			name = MacCleanerPro;
			productName = MacCleanerPro;
			productReference = B8E1A1003 /* MacCleanerPro.app */;
			productType = "com.apple.product-type.application";
		};
		B8E1A1011 /* MacCleanerProApp.swift in Sources */ = {
			isa = PBXBuildFile;
			fileRef = B8E1A1001 /* MacCleanerProApp.swift */;
		};
		B8E1A1012 /* ContentView.swift in Sources */ = {
			isa = PBXBuildFile;
			fileRef = B8E1A1002 /* ContentView.swift */;
		};
		B8E1A1013 /* Project object */ = {
			isa = PBXProject;
			attributes = {
				LastSwiftUpdateCheck = 1500;
				LastUpgradeCheck = 1500;
				TargetAttributes = {
					B8E1A1010 = {
						CreatedOnToolsVersion = 15.0;
					};
				};
			};
			buildConfigurationList = B8E1A1021 /* Build configuration list for PBXProject "MacCleanerPro" */;
			compatibilityVersion = "Xcode 14.0";
			developmentRegion = en;
			hasScannedForEncodings = 0;
			knownRegions = (
				en,
			);
			mainGroup = B8E1A1009;
			productRefGroup = B8E1A1008 /* Products */;
			projectDirPath = "";
			projectRoot = "";
			targets = (
				B8E1A1010 /* MacCleanerPro */,
			);
		};
		B8E1A1014 /* Debug */ = {
			isa = XCBuildConfiguration;
			buildSettings = {
				ALWAYS_SEARCH_USER_PATHS = NO;
				CLANG_ANALYZER_NONNULL = YES;
				CLANG_CXX_LANGUAGE_STANDARD = "gnu++20";
				CLANG_ENABLE_MODULES = YES;
				CLANG_ENABLE_OBJC_ARC = YES;
				CLANG_WARN_BOOL_CONVERSION = YES;
				CLANG_WARN_CONSTANT_CONVERSION = YES;
				CLANG_WARN_EMPTY_BODY = YES;
				CLANG_WARN_ENUM_CONVERSION = YES;
				CLANG_WARN_INT_CONVERSION = YES;
				CLANG_WARN_UNREACHABLE_CODE = YES;
				COPY_PHASE_STRIP = NO;
				DEBUG_INFORMATION_FORMAT = dwarf;
				ENABLE_STRICT_OBJC_MSGSEND = YES;
				ENABLE_TESTABILITY = YES;
				GCC_C_LANGUAGE_STANDARD = gnu11;
				GCC_DYNAMIC_NO_PIC = NO;
				GCC_NO_COMMON_BLOCKS = YES;
				GCC_OPTIMIZATION_LEVEL = 0;
				GCC_PREPROCESSOR_DEFINITIONS = (
					"DEBUG=1",
					"$(inherited)",
				);
				GCC_WARN_64_TO_32_BIT_CONVERSION = YES;
				GCC_WARN_ABOUT_RETURN_TYPE = YES_ERROR;
				GCC_WARN_UNDECLARED_SELECTOR = YES;
				GCC_WARN_UNINITIALIZED_AUTOS = YES_AGGRESSIVE;
				GCC_WARN_UNUSED_FUNCTION = YES;
				GCC_WARN_UNUSED_VARIABLE = YES;
				MACOSX_DEPLOYMENT_TARGET = 13.0;
				MTL_ENABLE_DEBUG_INFO = INCLUDE_SOURCE;
				MTL_FAST_MATH = YES;
				ONLY_ACTIVE_ARCH = YES;
				SDKROOT = macosx;
				SWIFT_ACTIVE_COMPILATION_CONDITIONS = DEBUG;
				SWIFT_OPTIMIZATION_LEVEL = "-Onone";
			};
			name = Debug;
		};
		B8E1A1015 /* Release */ = {
			isa = XCBuildConfiguration;
			buildSettings = {
				ALWAYS_SEARCH_USER_PATHS = NO;
				CLANG_ANALYZER_NONNULL = YES;
				CLANG_CXX_LANGUAGE_STANDARD = "gnu++20";
				CLANG_ENABLE_MODULES = YES;
				CLANG_ENABLE_OBJC_ARC = YES;
				CLANG_WARN_BOOL_CONVERSION = YES;
				CLANG_WARN_CONSTANT_CONVERSION = YES;
				CLANG_WARN_EMPTY_BODY = YES;
				CLANG_WARN_ENUM_CONVERSION = YES;
				CLANG_WARN_INT_CONVERSION = YES;
				CLANG_WARN_UNREACHABLE_CODE = YES;
				COPY_PHASE_STRIP = NO;
				DEBUG_INFORMATION_FORMAT = "dwarf-with-dsym";
				ENABLE_NS_ASSERTIONS = NO;
				ENABLE_STRICT_OBJC_MSGSEND = YES;
				GCC_C_LANGUAGE_STANDARD = gnu11;
				GCC_NO_COMMON_BLOCKS = YES;
				GCC_WARN_64_TO_32_BIT_CONVERSION = YES;
				GCC_WARN_ABOUT_RETURN_TYPE = YES_ERROR;
				GCC_WARN_UNDECLARED_SELECTOR = YES;
				GCC_WARN_UNINITIALIZED_AUTOS = YES_AGGRESSIVE;
				GCC_WARN_UNUSED_FUNCTION = YES;
				GCC_WARN_UNUSED_VARIABLE = YES;
				MACOSX_DEPLOYMENT_TARGET = 13.0;
				MTL_ENABLE_DEBUG_INFO = NO;
				MTL_FAST_MATH = YES;
				SDKROOT = macosx;
				SWIFT_COMPILATION_MODE = wholemodule;
				SWIFT_OPTIMIZATION_LEVEL = "-O";
			};
			name = Release;
		};
		B8E1A1016 /* Debug */ = {
			isa = XCBuildConfiguration;
			buildSettings = {
				CODE_SIGN_STYLE = Automatic;
				COMBINE_HIDPI_IMAGES = YES;
				CURRENT_PROJECT_VERSION = 1;
				ENABLE_PREVIEWS = YES;
				GENERATE_INFOPLIST_FILE = YES;
				INFOPLIST_KEY_NSHumanReadableCopyright = "";
				LD_RUNPATH_SEARCH_PATHS = (
					"$(inherited)",
					"@executable_path/../Frameworks",
				);
				MARKETING_VERSION = 1.0;
				PRODUCT_BUNDLE_IDENTIFIER = "com.maccleaner.MacCleanerPro";
				PRODUCT_NAME = "$(TARGET_NAME)";
				SWIFT_EMIT_LOC_STRINGS = YES;
				SWIFT_VERSION = 5.0;
			};
			name = Debug;
		};
		B8E1A1017 /* Release */ = {
			isa = XCBuildConfiguration;
			buildSettings = {
				CODE_SIGN_STYLE = Automatic;
				COMBINE_HIDPI_IMAGES = YES;
				CURRENT_PROJECT_VERSION = 1;
				ENABLE_PREVIEWS = YES;
				GENERATE_INFOPLIST_FILE = YES;
				INFOPLIST_KEY_NSHumanReadableCopyright = "";
				LD_RUNPATH_SEARCH_PATHS = (
					"$(inherited)",
					"@executable_path/../Frameworks",
				);
				MARKETING_VERSION = 1.0;
				PRODUCT_BUNDLE_IDENTIFIER = "com.maccleaner.MacCleanerPro";
				PRODUCT_NAME = "$(TARGET_NAME)";
				SWIFT_EMIT_LOC_STRINGS = YES;
				SWIFT_VERSION = 5.0;
			};
			name = Release;
		};
		B8E1A1020 /* Build configuration list for PBXNativeTarget "MacCleanerPro" */ = {
			isa = XCConfigurationList;
			buildConfigurations = (
				B8E1A1016 /* Debug */,
				B8E1A1017 /* Release */,
			);
			defaultConfigurationIsVisible = 0;
			defaultConfigurationName = Release;
		};
		B8E1A1021 /* Build configuration list for PBXProject "MacCleanerPro" */ = {
			isa = XCConfigurationList;
			buildConfigurations = (
				B8E1A1014 /* Debug */,
				B8E1A1015 /* Release */,
			);
			defaultConfigurationIsVisible = 0;
			defaultConfigurationName = Release;
		};
	};
	rootObject = B8E1A1013 /* Project object */;
}
PBXEOF

echo "✅ Fichier projet créé"
