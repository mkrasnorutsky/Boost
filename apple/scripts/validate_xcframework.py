#!/usr/bin/env python3
"""Link representative FlightGear/SimGear Boost APIs on every slice and run natively."""
from pathlib import Path
import plistlib,subprocess,tempfile
ROOT=Path(__file__).resolve().parents[2]
import os
WORK=Path(os.environ.get("APPLE_BUILD_ROOT", str(ROOT))).expanduser().resolve()
artifact=WORK/'dist/Boost.xcframework'
info=plistlib.loads((artifact/'Info.plist').read_bytes())
assert len(info['AvailableLibraries'])==2
with tempfile.TemporaryDirectory(prefix='boost-validation-') as temp:
    temp=Path(temp)
    for entry in info['AvailableLibraries']:
        sim=entry.get('SupportedPlatformVariant')=='simulator'
        assert entry['SupportedPlatform']=='ios'
        assert set(entry['SupportedArchitectures'])==({'arm64','x86_64'} if sim else {'arm64'})
        folder=artifact/entry['LibraryIdentifier'];library=folder/entry['LibraryPath'];headers=folder/entry['HeadersPath']
        subprocess.run(['lipo',str(library),'-verify_arch',*entry['SupportedArchitectures']],check=True)
        assert (headers/'boost/version.hpp').read_bytes()==(ROOT/'boost/version.hpp').read_bytes()
        for arch in entry['SupportedArchitectures']:
            triple=arch+'-apple-ios18.0'+('-simulator' if sim else '')
            sdk=subprocess.check_output(['xcrun','--sdk','iphonesimulator' if sim else 'iphoneos','--show-sdk-path'],text=True).strip()
            subprocess.run(['xcrun','clang++','-std=c++17','-target',triple,'-isysroot',sdk,'-I'+str(headers),str(ROOT/'apple/scripts/boost_smoke.cpp'),str(library),'-o',str(temp/triple)],check=True)
            print('PASS: API compilation and linking '+triple,flush=True)
    subprocess.run(['xcrun','clang','-c',str(ROOT/'apple/anchor.c'),'-o',str(temp/'anchor.o')],check=True)
    subprocess.run(['xcrun','clang++','-std=c++17','-I'+str(ROOT),str(ROOT/'apple/scripts/boost_smoke.cpp'),str(temp/'anchor.o'),'-o',str(temp/'native')],check=True)
    subprocess.run([str(temp/'native')],check=True)
    print('PASS: native bimap, multi-index, optional, lexical cast, tokenizer and XML behavior')
