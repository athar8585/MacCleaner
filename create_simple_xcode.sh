#!/bin/bash

# 🍎 MacCleaner Pro - Créateur de Projet Xcode Simple et Fonctionnel
# Crée un projet Xcode qui build correctement

echo "🍎 CRÉATION PROJET XCODE SIMPLIFIÉ"
echo "=================================="

PROJECT_NAME="MacCleanerPro"
PROJECT_DIR="/Users/loicdeloison/Desktop/MacCleaner/XcodeSimple"

# Nettoyer et recréer le répertoire
rm -rf "$PROJECT_DIR"
mkdir -p "$PROJECT_DIR"
cd "$PROJECT_DIR"

echo "📁 Génération projet avec xcodebuild..."

# Créer un nouveau projet macOS avec xcodebuild
cat > create_project.sh << 'EOF'
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
EOF

chmod +x create_project.sh
./create_project.sh

echo "✅ Structure projet créée"
echo "📝 Création des fichiers Swift..."

# Créer le fichier App principal (simplifié)
cat > "$PROJECT_NAME/MacCleanerProApp.swift" << 'SWIFTEOF'
//
//  MacCleanerProApp.swift
//  MacCleanerPro
//
//  Point d'entrée de l'application
//

import SwiftUI

@main
struct MacCleanerProApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
                .frame(minWidth: 900, minHeight: 600)
        }
        .windowStyle(.titleBar)
    }
}
SWIFTEOF

# Créer la vue principale (simplifiée pour éviter les erreurs)
cat > "$PROJECT_NAME/ContentView.swift" << 'SWIFTEOF'
//
//  ContentView.swift
//  MacCleanerPro
//
//  Interface principale
//

import SwiftUI

struct ContentView: View {
    @State private var selectedTab = 0
    @State private var scanProgress: Double = 0.0
    @State private var isScanning = false
    
    var body: some View {
        NavigationSplitView {
            // Sidebar
            List {
                NavigationLink(destination: DashboardView()) {
                    Label("Dashboard", systemImage: "house.fill")
                }
                
                NavigationLink(destination: CleaningView(scanProgress: $scanProgress, isScanning: $isScanning)) {
                    Label("Nettoyage", systemImage: "trash.circle.fill")
                }
                
                NavigationLink(destination: SecurityView()) {
                    Label("Sécurité", systemImage: "shield.checkered")
                }
                
                NavigationLink(destination: MonitoringView()) {
                    Label("Monitoring", systemImage: "chart.line.uptrend.xyaxis")
                }
            }
            .navigationTitle("MacCleaner Pro")
            
        } detail: {
            DashboardView()
        }
    }
}

struct DashboardView: View {
    var body: some View {
        VStack(spacing: 24) {
            // Header
            HStack {
                Image(systemName: "macbook")
                    .font(.system(size: 48))
                    .foregroundColor(.blue)
                
                VStack(alignment: .leading) {
                    Text("MacCleaner Pro")
                        .font(.largeTitle)
                        .fontWeight(.bold)
                    
                    Text("Votre Mac fonctionne parfaitement")
                        .font(.subheadline)
                        .foregroundColor(.secondary)
                }
                
                Spacer()
            }
            .padding()
            
            // Cartes d'informations
            LazyVGrid(columns: [
                GridItem(.flexible()),
                GridItem(.flexible()),
                GridItem(.flexible())
            ], spacing: 16) {
                
                InfoCard(title: "Stockage", value: "125 GB", total: "500 GB", icon: "externaldrive", color: .blue)
                InfoCard(title: "Mémoire", value: "8.2 GB", total: "16 GB", icon: "memorychip", color: .green)
                InfoCard(title: "CPU", value: "25%", total: "100%", icon: "cpu", color: .orange)
            }
            .padding()
            
            Spacer()
        }
        .frame(maxWidth: .infinity, maxHeight: .infinity)
        .background(Color(NSColor.controlBackgroundColor))
    }
}

struct CleaningView: View {
    @Binding var scanProgress: Double
    @Binding var isScanning: Bool
    
    var body: some View {
        VStack(spacing: 24) {
            Text("🧹 Nettoyage intelligent")
                .font(.largeTitle)
                .fontWeight(.bold)
            
            if isScanning {
                ProgressView(value: scanProgress)
                    .progressViewStyle(.linear)
                    .padding()
                
                Text("Analyse en cours... \(Int(scanProgress * 100))%")
                    .foregroundColor(.secondary)
            }
            
            Button(action: startScan) {
                Label("Démarrer l'analyse", systemImage: "magnifyingglass")
            }
            .buttonStyle(.borderedProminent)
            .disabled(isScanning)
            
            Spacer()
        }
        .padding()
    }
    
    private func startScan() {
        isScanning = true
        scanProgress = 0.0
        
        Timer.scheduledTimer(withTimeInterval: 0.1, repeats: true) { timer in
            scanProgress += 0.02
            if scanProgress >= 1.0 {
                timer.invalidate()
                isScanning = false
            }
        }
    }
}

struct SecurityView: View {
    var body: some View {
        VStack {
            Image(systemName: "shield.checkered")
                .font(.system(size: 64))
                .foregroundColor(.blue)
            
            Text("Scanner de sécurité")
                .font(.title)
                .fontWeight(.bold)
            
            Text("Protection temps réel")
                .foregroundColor(.secondary)
        }
    }
}

struct MonitoringView: View {
    var body: some View {
        VStack {
            Image(systemName: "chart.line.uptrend.xyaxis")
                .font(.system(size: 64))
                .foregroundColor(.green)
            
            Text("Monitoring système")
                .font(.title)
                .fontWeight(.bold)
            
            Text("Surveillance en temps réel")
                .foregroundColor(.secondary)
        }
    }
}

struct InfoCard: View {
    let title: String
    let value: String
    let total: String
    let icon: String
    let color: Color
    
    var body: some View {
        VStack(spacing: 8) {
            Image(systemName: icon)
                .font(.system(size: 24))
                .foregroundColor(color)
            
            Text(title)
                .font(.caption)
                .foregroundColor(.secondary)
            
            Text(value)
                .font(.title2)
                .fontWeight(.semibold)
            
            Text("/ \(total)")
                .font(.caption2)
                .foregroundColor(.secondary)
        }
        .frame(maxWidth: .infinity)
        .padding()
        .background(Color(NSColor.windowBackgroundColor))
        .cornerRadius(8)
    }
}

#Preview {
    ContentView()
}
SWIFTEOF

echo "✅ Fichiers Swift créés"
echo ""
echo "🚀 PROJET PRÊT !"
echo "📂 Emplacement: $PROJECT_DIR"
echo ""
echo "🔧 POUR TESTER :"
echo "1. cd $PROJECT_DIR"  
echo "2. open MacCleanerPro.xcodeproj"
echo "3. Appuyer sur ▶️ (Run) dans Xcode"
echo ""
echo "✅ Cette version devrait build sans erreur !"