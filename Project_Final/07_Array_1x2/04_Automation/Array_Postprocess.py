"""Generate and verify the complete result package from saved native CST outputs."""
from Array_Results_Extraction import ROOT,W,R,P,C,DOC
import Array_Results_Extraction,Array_Comparison,Array_Coupling,Array_Current_Maps,Array_Common_Reference,Array_Report,Array_Config_Check,Array_Power_Closure,Array_Delivery
def main():
    from Array_Final_Selection import call
    if not list(R.glob('CST_50ohm*.s1p')):call('Array_Touchstone.py')
    for stage in [Array_Results_Extraction.main,Array_Comparison.run,Array_Coupling.run,Array_Current_Maps.run,Array_Common_Reference.main,Array_Report.main,Array_Config_Check.main,Array_Power_Closure.main,Array_Delivery.main]:
        print(stage.__module__,flush=True);stage()
    print('DELIVERY_CHECKED',ROOT,flush=True)
if __name__=='__main__':main()

