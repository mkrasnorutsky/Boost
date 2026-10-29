#!/usr/bin/env python3
"""Package the complete Boost 1.86 header tree for iOS and Simulator."""
from pathlib import Path
import json,shutil,subprocess
ROOT=Path(__file__).resolve().parents[2]
import os
WORK=Path(os.environ.get("APPLE_BUILD_ROOT", str(ROOT))).expanduser().resolve()
def run(*args):
    print('+',*map(str,args),flush=True)
    subprocess.run(list(map(str,args)),check=True)
def main():
    out=WORK/'dist';out.mkdir(exist_ok=True);stage=out/'staging'
    if stage.exists():shutil.rmtree(stage)
    stage.mkdir();headers=stage/'Headers'
    shutil.copytree(ROOT/'boost',headers/'boost')
    (headers/'CBoost.h').write_text('#pragma once\n#ifdef __cplusplus\nextern "C" {\n#endif\nunsigned int OneClickPilotBoostVersion(void);\n#ifdef __cplusplus\n}\n#endif\n')
    # Boost headers are C++ templates. Do not implicitly modularize the entire tree.
    (headers/'CBoost').mkdir(exist_ok=True)
    (headers/'CBoost/module.modulemap').write_text('module CBoost { header "../CBoost.h" export * }\n')
    libraries={}
    variants=[('ios-arm64','iphoneos','arm64'),('simulator-arm64','iphonesimulator','arm64'),('simulator-x86_64','iphonesimulator','x86_64')]
    for name,sdk,arch in variants:
        folder=WORK/'out'/name;folder.mkdir(parents=True,exist_ok=True)
        sdkpath=subprocess.check_output(['xcrun','--sdk',sdk,'--show-sdk-path'],text=True).strip()
        triple=arch+'-apple-ios18.0'+('-simulator' if sdk=='iphonesimulator' else '')
        run('xcrun','clang','-target',triple,'-isysroot',sdkpath,'-O2','-c',ROOT/'apple/anchor.c','-o',folder/'anchor.o')
        libraries[name]=folder/'libboost_headers.a'
        run('xcrun','libtool','-static','-o',libraries[name],folder/'anchor.o')
    universal=stage/'libboost_headers.a'
    run('lipo','-create',libraries['simulator-arm64'],libraries['simulator-x86_64'],'-output',universal)
    artifact=out/'Boost.xcframework'
    if artifact.exists():shutil.rmtree(artifact)
    run('xcodebuild','-create-xcframework','-library',libraries['ios-arm64'],'-headers',headers,'-library',universal,'-headers',headers,'-output',artifact)
    shutil.copy2(ROOT/'LICENSE_1_0.txt',artifact/'LICENSE_1_0.txt')
    manifest={'source_revision':subprocess.check_output(['git','-C',str(ROOT),'rev-parse','HEAD'],text=True).strip(), 'upstream':json.loads((ROOT/'apple/source.json').read_text()),'minimum_ios':'18.0','slices':[v[0] for v in variants],'content':'Complete Boost header tree and version anchor; no compiled Boost component libraries','header_count':sum(1 for p in (ROOT/'boost').rglob('*') if p.is_file())}
    (out/'build-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
if __name__=='__main__':main()
