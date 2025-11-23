# test_complete_system.py
# AI-generated code section begins - GitHub Copilot assisted with comprehensive system testing

from router import analyze_transcript

def test_complete_system():
    """Comprehensive test of the complete medical referral system"""
    
    print("🧪 COMPREHENSIVE SYSTEM TEST")
    print("=" * 50)
    
    # Test Case 1: Cardiology referral with complete patient data
    print("\n📋 TEST CASE 1: Cardiology Referral")
    test1 = '''
    I need to refer John Smith to cardiology. He is a 48 year old male, date of birth is 03/15/1975. 
    He has been complaining of chest pain with exertion and shortness of breath. 
    The patient reports these episodes occur during physical activity and resolve with rest. 
    He also mentions palpitations and some dizziness. 
    No radiation of pain to arms or jaw, but increased frequency over the past 2 weeks.
    '''
    
    result1 = analyze_transcript(test1)
    print(f"Result: {'✅ SUCCESS' if result1 else '❌ FAILED'}")
    
    # Test Case 2: Dermatology referral with female patient
    print("\n📋 TEST CASE 2: Dermatology Referral")
    test2 = '''
    Please refer Sarah Johnson to dermatology. She is 35 years old, female, DOB 07/22/1988.
    She has been experiencing skin rash on her arms and legs with itching. 
    The rash appeared about 2 weeks ago and has been getting worse.
    '''
    
    result2 = analyze_transcript(test2)
    print(f"Result: {'✅ SUCCESS' if result2 else '❌ FAILED'}")
    
    # Test Case 3: Orthopedics referral with minimal data
    print("\n📋 TEST CASE 3: Orthopedics Referral (Minimal Data)")
    test3 = '''
    Need to refer Michael Brown to orthopedics for knee pain and possible injury.
    '''
    
    result3 = analyze_transcript(test3)
    print(f"Result: {'✅ SUCCESS' if result3 else '❌ FAILED'}")
    
    print("\n" + "=" * 50)
    print(f"OVERALL TEST RESULTS:")
    print(f"Tests Passed: {sum([result1, result2, result3])}/3")
    print(f"System Status: {'✅ FULLY OPERATIONAL' if all([result1, result2, result3]) else '⚠️ NEEDS ATTENTION'}")

if __name__ == "__main__":
    test_complete_system()

# AI-generated code section ends
