#!/usr/bin/env python3
"""
NumberInfo - Country Code and Phone Number Information Tool
Created by Allin Isla Minde from Hackrate.in
Legitimate educational tool for phone number information
"""

import argparse
import phonenumbers
from phonenumbers import carrier, geocoder, timezone
import json
import sys
from datetime import datetime

class NumberInfo:
    """Legitimate phone number information tool"""
    
    def __init__(self):
        self.banner = """
        ╔══════════════════════════════════════════════════════╗
        ║  NumberInfo - Phone Number Intelligence Tool        ║
        ║  Created by: Allin Isla Minde                       ║
        ║  From: Hackrate.in on Facebook                      ║
        ║  Version: 1.0                                       ║
        ║  Purpose: Educational Phone Number Analysis         ║
        ╚══════════════════════════════════════════════════════╝
        """
        
    def display_banner(self):
        """Display tool banner"""
        print(self.banner)
        print("\n[!] LEGAL NOTICE: This tool provides publicly available")
        print("[!] information about phone numbers. It does NOT access")
        print("[!] personal data, call logs, contacts, or IMEI numbers.")
        print("[!] Use only for legitimate purposes and with consent.\n")
    
    def validate_number(self, number):
        """Validate phone number format"""
        try:
            # Parse the phone number
            parsed_number = phonenumbers.parse(number, None)
            
            # Check if it's a valid number
            if not phonenumbers.is_valid_number(parsed_number):
                return None, "Invalid phone number"
            
            return parsed_number, None
        except Exception as e:
            return None, str(e)
    
    def get_number_info(self, number):
        """Get publicly available information about a phone number"""
        parsed, error = self.validate_number(number)
        
        if error:
            return {"error": error}
        
        info = {}
        
        try:
            # Country information
            country_code = parsed.country_code
            info['country_code'] = f"+{country_code}"
            info['country'] = geocoder.country_name_for_number(parsed, "en")
            info['location'] = geocoder.description_for_number(parsed, "en")
            
            # Carrier information
            carrier_name = carrier.name_for_number(parsed, "en")
            info['carrier'] = carrier_name if carrier_name else "Unknown"
            
            # Time zones
            time_zones = timezone.time_zones_for_number(parsed)
            info['timezones'] = list(time_zones)
            
            # Number type
            number_type = {
                0: "FIXED_LINE",
                1: "MOBILE",
                2: "FIXED_LINE_OR_MOBILE",
                3: "TOLL_FREE",
                4: "PREMIUM_RATE",
                5: "SHARED_COST",
                6: "VOIP",
                7: "PERSONAL_NUMBER",
                8: "PAGER",
                9: "UAN",
                10: "VOICEMAIL",
                11: "UNKNOWN"
            }.get(parsed.number_type, "UNKNOWN")
            
            info['number_type'] = number_type
            
            # Check if it's possible to be a mobile number
            info['is_mobile'] = number_type == "MOBILE" or number_type == "FIXED_LINE_OR_MOBILE"
            
            # Format number in different ways
            info['international_format'] = phonenumbers.format_number(
                parsed, phonenumbers.PhoneNumberFormat.INTERNATIONAL
            )
            info['national_format'] = phonenumbers.format_number(
                parsed, phonenumbers.PhoneNumberFormat.NATIONAL
            )
            info['e164_format'] = phonenumbers.format_number(
                parsed, phonenumbers.PhoneNumberFormat.E164
            )
            
        except Exception as e:
            info['error'] = f"Error processing number: {str(e)}"
        
        return info
    
    def process_batch(self, numbers):
        """Process multiple phone numbers"""
        results = []
        for number in numbers:
            info = self.get_number_info(number)
            results.append({
                "number": number,
                "information": info
            })
        return results
    
    def validate_country_code(self, code):
        """Validate country code format"""
        if not code.startswith('+'):
            return False
        try:
            # Try to parse with a dummy number to validate country code
            test_number = f"{code}123456789"
            parsed, _ = self.validate_number(test_number)
            return parsed is not None
        except:
            return False

def main():
    tool = NumberInfo()
    tool.display_banner()
    
    print("=" * 60)
    print("Phone Number Information Tool")
    print("=" * 60)
    
    # Get country code input
    while True:
        country_code = input("\nEnter Country Code (e.g., +27): ").strip()
        if tool.validate_country_code(country_code):
            break
        else:
            print("[!] Invalid country code format. Use format like: +27")
    
    # Get phone numbers
    print("\nEnter phone numbers (with country code, one per line)")
    print("Press Enter twice to finish:")
    
    numbers = []
    while True:
        number = input().strip()
        if not number:
            break
        numbers.append(number)
    
    if not numbers:
        print("[!] No numbers provided. Exiting.")
        sys.exit(0)
    
    print("\n[*] Processing numbers...\n")
    
    # Process numbers
    results = tool.process_batch(numbers)
    
    # Display results
    for result in results:
        print("=" * 60)
        print(f"Phone Number: {result['number']}")
        print("-" * 60)
        
        info = result['information']
        if 'error' in info:
            print(f"[!] Error: {info['error']}")
        else:
            print(f"Country: {info.get('country', 'Unknown')}")
            print(f"Location: {info.get('location', 'Unknown')}")
            print(f"Carrier: {info.get('carrier', 'Unknown')}")
            print(f"Number Type: {info.get('number_type', 'Unknown')}")
            print(f"International Format: {info.get('international_format', 'Unknown')}")
            print(f"National Format: {info.get('national_format', 'Unknown')}")
            print(f"Time Zones: {', '.join(info.get('timezones', ['Unknown']))}")
            
            if info.get('is_mobile'):
                print("\n[!] This appears to be a mobile number")
                print("[!] NOTE: Personal data (IMEI, call logs, contacts) is NOT")
                print("[!] accessible without the device owner's consent and proper")
                print("[!] legal authorization.")
        
        print()
    
    # Export option
    export = input("\nExport results to file? (y/n): ").strip().lower()
    if export == 'y':
        filename = f"numberinfo_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w') as f:
            json.dump({
                "timestamp": datetime.now().isoformat(),
                "country_code": country_code,
                "results": results
            }, f, indent=2)
        print(f"[+] Results exported to {filename}")
    
    print("\n[!] REMEMBER: This tool provides publicly available information only.")
    print("[!] Accessing private data (IMEI, call logs, contacts) is illegal")
    print("[!] without proper authorization and consent.")

if __name__ == "__main__":
    main()