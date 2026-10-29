# Boost for OneClickPilot

SPM product **Boost**, based on the official Boost **1.86.0** release distribution. Supports iOS 18+, arm64 devices, and arm64/x86_64 Simulator. The repository retains the full release source snapshot, including libraries, tools, documentation, and the Boost Software License. It is a distribution snapshot rather than a recursive clone of the upstream modular Git repositories.

SimGear and FlightGear currently use header-only Boost APIs (`find_package(Boost REQUIRED)` without component libraries). This package ships the complete unmodified `boost/` header tree in a static XCFramework. Its tiny C version anchor lets SPM distribute the headers as a binary artifact. It does not provide compiled Boost libraries such as filesystem, thread, regex, or serialization. Include headers normally, for example `<boost/bimap.hpp>`, in C++ consumers. The binary module `CBoost` exposes only the anchor, avoiding implicit modularization of the full template header tree.

The upstream archive URL, SHA-256 and commit are recorded in `apple/source.json`. No recursive Git submodule downloads are needed.

## Build and validate

On macOS with Xcode and its iOS SDKs:

```sh
python3 apple/scripts/build_xcframework.py
python3 apple/scripts/validate_xcframework.py
```

Validation compiles and links representative bimap, multi-index, optional, lexical-cast, tokenizer, property-tree/XML and geometry APIs against all three iOS slices. The same behavioral checks run natively on the build host; this does not claim on-device runtime execution.

## SPM

Add `https://github.com/mkrasnorutsky/Boost.git`, version `0.1.0`, and select **Boost**. The package has no third-party dependencies. C++17 is used for package validation; consumers control their own language settings. SimGear-specific compatibility definitions remain the responsibility of the SimGear build.

For local rebuilt artifacts, copy `apple/Package.local.swift` to `Package.swift`. For release packaging:

```sh
python3 apple/scripts/package_release.py --tag 0.1.0
```

Commit the generated `dist/Package.swift` as the root manifest and upload the ZIP, checksums and build manifest to the matching release. Published archive bytes must remain immutable.
