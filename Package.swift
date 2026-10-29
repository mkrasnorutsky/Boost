// swift-tools-version: 5.9
import PackageDescription
let package = Package(name: "Boost", platforms: [.iOS("18.0")],
    products: [.library(name: "Boost", targets: ["Boost"])],
    targets: [
        .binaryTarget(name: "CBoost", url: "https://github.com/mkrasnorutsky/Boost/releases/download/0.1.1/Boost.xcframework.zip", checksum: "3135525aa0368d05c8fd76109a5f80c5023194b3898b7a904d24ccb04cd602b6"),
        .target(name: "Boost", dependencies: ["CBoost"], path: "apple/SPM", publicHeadersPath: "include")
    ], cxxLanguageStandard: .cxx17)
