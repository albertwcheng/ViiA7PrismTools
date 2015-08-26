

if [ $# -lt 3 ]; then
echo $0 filename gene sample
exit 1
fi

filename=$1
gene=$2
sample=(`echo $3 | tr "," " "`)

for((i=0;i<${#sample[@]};i++));do
#echo ${sample[$i]}
SAMPLENAME[$i]="${sample[$i]} x x"
SAMPLEDATA[$i]=`awk -v FS="\t" -v OFS="\t" -v sample=${sample[$i]} '$4==sample' $filename | grep $gene | cut -f9,10,11 | sort | uniq`
done

echo ${SAMPLENAME[@]}
echo ${SAMPLEDATA[@]}