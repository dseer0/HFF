import subprocess
import time
from subprocess import Popen
import os
import zipfile

def installFromReq(dir): 
  start = time.time()
  subprocess.run("pip install --progress-bar off -r reg.txt --target " + dir, check=True)
  end = time.time()
  print("seconds with cache: " + str(start - end))


# 12 sekund, proba 3 razy
def wheel(dir):
  start = time.time()
  subprocess.run(f"pip wheel --prefer-binary --wheel-dir={dir} -r reg.txt", check=True)
  end = time.time()
  print("wheel seconds with cache: " + str(end - start))


#95 sekund, 97sekund
#72
#wyrzucic no-compile
def pipInstallWheels(wheelDir, toWhere):
  start = time.time()
  subprocess.run(f"pip install --no-index --find-links={wheelDir} -r reg.txt --target {toWhere}", check=True)
  end = time.time()
  print("pip install wheelswith cache: " + str(end - start))   


def listWheels(wheelDir):
  return os.listdir(wheelDir)
  
  #60, 50, 60 bez --no-compile
  # 17s,  55s, 25s, 51s  z no-compile
def pipInstallAsync(wheels, wheelDir, toWhere):
  start = time.time()
  prcs = []
  for wheel in wheels:
    p = Popen(f"pip install --no-compile --no-index --no-deps --target {toWhere}/{wheel}-dir {wheelDir}/{wheel}")
    prcs.append(p)
  for p in prcs:
    p.wait()
  end = time.time()
  print("pip async in s: " + str(end - start))

def unzip(wheels, wheelDir, toWhere):
  start = time.time()
  prcs = []
  for wheel in wheels:
    with zipfile.ZipFile(f"{wheelDir}/{wheel}", 'r') as zip_ref:
      zip_ref.extractall(f"{toWhere}")
  end = time.time()
  print("unzip  in s: " + str(end - start))


def download(dir):
  start = time.time()
  subprocess.run(f"pip download -d {dir} --only-binary=:all: -r reg.txt", check=True)
  end = time.time()
  print("download seconds with cache: " + str(end - start))

def createPth(wheels, whereInstalled):
  paths = [os.path.abspath(f"{whereInstalled}/{x}-dir") for x in wheels]
  string = '\n'.join(paths)
  f = open("libs.pth", "w")
  f.write(string)
  f.close()


# pip cache remove *
wheel("wheels")
# download("downloaded3344")
wheels = listWheels("wheels")
# print(wheels)
# pipInstallAsync(wheels, "wheels", "installed")
# createPth(wheels, "installed")
# unzip(wheels, "wheels", "installedunziper")

pipInstallWheels("wheels", "installed344456")


# installFromReq("from_req")

#torch wheels - 38sekund, pipasync 46sekundy z bledem!!!, 