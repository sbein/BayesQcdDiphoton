python prepinput.py T6Wg
python runlimits.py T6Wg
python Get2DContour.py --model=T6Wg --box=diphoton
find * -name T6Wg_diphoton_results.root
mv limits2root/results/T6Wg_diphoton_results.root SMSPlottingCode/syst_results/diphoton/T6Wg_diphoton_results.root
echo cd SMSPlottingCode


python prepinput.py T5Wg
python runlimits.py T5Wg
python Get2DContour.py --model=T5Wg --box=diphoton
find * -name T5Wg_diphoton_results.root
mv limits2root/results/T5Wg_diphoton_results.root SMSPlottingCode/syst_results/diphoton/T5Wg_diphoton_results.root
cd SMSPlottingCode
python scripts/makeSMSplots.py config/diphoton/T5Wg_diphoton_exp.cfg T5WgSep30



