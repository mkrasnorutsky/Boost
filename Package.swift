// swift-tools-version: 5.9
import PackageDescription
let package = Package(name: "Boost", platforms: [.iOS("18.0")],
    products: [.library(name: "Boost", targets: ["Boost"])],
    targets: [
        .binaryTarget(name: "CBoost", url: "https://github.com/mkrasnorutsky/Boost/releases/download/0.1.0/Boost.xcframework.zip", checksum: "b5cda409e33df01f00e7bbda3ac7bf7853efad4b49bbdb9764b29f351e352387"),
        .target(name: "Boost", dependencies: ["CBoost"], path: "apple/SPM", publicHeadersPath: "include")
    ], cxxLanguageStandard: .cxx17)
