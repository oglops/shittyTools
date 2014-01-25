shittyTools
===========

shitty tools i wrote over the years

mayaFileConverter.py
-----

脑残作，写完了才发现根本没用。因为一开始是觉得.mb打开再存.ma再改好麻烦（有时候不知怎么了，2012里开文件的时候选了ignore version照样打不开2013,2014的文件），所以就用hex editor打开.mb看了下版本号的位置，直接改（瞎猜的），结果是能开了，但是因为2012以上版本里新加的命令的某些flags，依然打不开...所以一点屌用都没有....

不过.ma的是可以的，因为我把2012不认识的那些flags可以删掉

目前知道的不认识的有
// Error: file: E:/shittyTools/2014_cube_2012.ma line 94: Invalid flag '-ch' // 
// Error: line 213: Invalid flag '-objectFilterShowInHUD' // 
