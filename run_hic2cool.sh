# https://github.com/4dn-dcic/hic2cool

#hic2cool convert \
#    "/home/brydo/juicer/BCM15034109081_BCM15034109082.juicer.hic" \
#    "/home/brydo/juicer/BCM15034109081_BCM15034109082.juicer.mcool" \
#    -p 22

# https://github.com/4dn-dcic/hic2cool/issues/60

py_hic2cool="/mnt/c/Users/brydo/My Documents/GitHub/PDXHiC_multiresistance/Brydon/hic2cool/py_hic2cool.py"

python "$hic2mcool" \
    --hic_file "/mnt/c/Users/brydo/My Documents/GitHub/PDXHiC_multiresistance/Brydon/hic_juicer/BCM15034109081_BCM15034109082.juicer.hic"\
    --mcool_file "/mnt/c/Users/brydo/My Documents/GitHub/PDXHiC_multiresistance/Brydon/hic_juicer/BCM15034109081_BCM15034109082.juicer.KR.mcool" \
    --data_type "observed" \
    --normalization "KR" \
    --temp_dir "/mnt/c/Users/brydo/My Documents/GitHub/PDXHiC_multiresistance/Brydon/hic_juicer/temp"
