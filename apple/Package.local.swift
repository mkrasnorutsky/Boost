// swift-tools-version: 5.9
import PackageDescription
let package = Package(name: "Boost", platforms: [.iOS("18.0")],
    products: [.library(name: "Boost", targets: ["Boost"])],
    targets: [
        .binaryTarget(name: "CBoost", path: "dist/Boost.xcframework"),
        .target(name: "Boost", dependencies: ["CBoost"], path: "apple/SPM", publicHeadersPath: "include")
    ], cxxLanguageStandard: .cxx17)
