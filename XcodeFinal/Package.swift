// swift-tools-version: 5.9
import PackageDescription

let package = Package(
    name: "MacCleanerPro",
    platforms: [
        .macOS(.v13)
    ],
    dependencies: [],
    targets: [
        .executableTarget(
            name: "MacCleanerPro",
            dependencies: []
        )
    ]
)
