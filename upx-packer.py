from __future__ import print_function
import sys, os, subprocess, time

py2 = str is bytes                    # check if Python2
# do some adjustments whether Python v2 or v3
if not py2:
    import PySimpleGUI as psg
else:
    import PySimpleGUI27 as psg

try:
    bin_dir = sys.argv[1]
except:
    bin_dir = psg.PopupGetFolder("UPX Compression of binaries",
                                "Enter folder:")

if not bin_dir:
    raise SystemExit("Cancel requested")

bin_dir = os.path.abspath(bin_dir)
print("UPX Compression of binaries in folder '%s'" % bin_dir)

tasks = []
file_count = 0
file_sizes = {}
t0 = time.time()
for root, _, files in os.walk(bin_dir):
    for f in files:
        f = f.lower()        # lower casing file name (Windows, stupid!)
        fname = os.path.join(root, f)
        file_sizes[fname] = os.stat(fname).st_size
        if not f.endswith((".exe", ".dll", "pyd")):   # we only handle these
            continue
        if f.endswith(".dll"):
            if f.startswith("python"):
                continue
            if f.startswith("vcruntime"):
                continue
            if f.startswith("msvcp"):
                continue
            if f.startswith("cldapi"):
                continue
        # make the upx invocation commannd
        cmd = 'UPX -9 "%s"' % fname
        t = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        tasks.append(t)
        file_count += 1

print("Started %i compressions out of %i total files ..." % (file_count, len(file_sizes.keys())), flush=True)

for t in tasks:
    t.wait()

t1 = time.time()
print("Finished in %g seconds." % (t1-t0), flush=True)
old_size = new_size = 0.0
for f in file_sizes.keys():
    old_size += file_sizes[f]
    new_size += os.stat(f).st_size
old_size *= 1./1024/1024
new_size *= 1./1024/1024
diff_size = old_size - new_size
diff_percent = diff_size / old_size
text = "\nFolder Compression Results (MB)\nbefore: {:.5}\nafter: {:.5}\nsavings: {:.5} ({:.2%})"
print(text.format(old_size, new_size, diff_size, diff_percent))