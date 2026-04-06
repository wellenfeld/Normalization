#!/usr/bin/env python3
"""
Multi-Language Unicode Normalization Test Suite

Tests normalization behavior across different programming languages and environments.
This helps identify inconsistencies that could lead to security vulnerabilities.
"""

import json
import subprocess
import tempfile
import os
import sys
import unicodedata
from pathlib import Path

class MultiLanguageNormalizationTester:
    def __init__(self):
        self.test_cases = self.load_test_cases()
        self.results = {}
        
    def load_test_cases(self):
        """Load comprehensive test cases for normalization"""
        return [
            # Basic ASCII (should be unchanged)
            {"input": "hello", "description": "Basic ASCII"},
            {"input": "admin123", "description": "ASCII with numbers"},
            
            # Latin-1 with accents
            {"input": "café", "description": "Latin-1 with acute"},
            {"input": "naïve", "description": "Latin-1 with diaeresis"},
            {"input": "résumé", "description": "Latin-1 multiple accents"},
            
            # NFC vs NFD forms
            {"input": "e\u0301", "description": "NFD: e + combining acute"},
            {"input": "a\u0308", "description": "NFD: a + combining diaeresis"},
            {"input": "o\u0302\u0301", "description": "NFD: o + combining circumflex + acute"},
            
            # Fullwidth characters
            {"input": "ａｄｍｉｎ", "description": "Fullwidth Latin letters"},
            {"input": "１２３", "description": "Fullwidth numbers"},
            {"input": "；｜＆", "description": "Fullwidth operators"},
            
            # Mathematical characters
            {"input": "𝗮𝗱𝗺𝗶𝗻", "description": "Mathematical bold"},
            {"input": "𝒶𝒹𝓂𝒾𝓃", "description": "Mathematical script"},
            {"input": "𝔞𝔡𝔪𝔦𝔫", "description": "Mathematical fraktur"},
            
            # Greek letters
            {"input": "αδμιν", "description": "Greek lowercase"},
            {"input": "ΑΔΜΙΝ", "description": "Greek uppercase"},
            
            # Cyrillic letters
            {"input": "аdмин", "description": "Mixed Cyrillic/Latin"},
            {"input": "АДМИН", "description": "Cyrillic uppercase"},
            
            # Turkish special characters
            {"input": "ıadmin", "description": "Turkish dotless I"},
            {"input": "İadmin", "description": "Turkish dotted capital I"},
            {"input": "paßword", "description": "German sharp S"},
            
            # Combining characters
            {"input": "data\u0305key", "description": "Combining overline"},
            {"input": "test\u0340data", "description": "Combining grave tone"},
            {"input": "test\u0341data", "description": "Combining acute tone"},
            
            # Invisible characters
            {"input": "user\u200Bsession", "description": "Zero width space"},
            {"input": "test\u200Cdata", "description": "Zero width non-joiner"},
            {"input": "test\u200Ddata", "description": "Zero width joiner"},
            {"input": "test\uFEFFdata", "description": "Zero width no-break space"},
            {"input": "test\u2060data", "description": "Word joiner"},
            
            # Bidirectional characters
            {"input": "admin\u202Etest", "description": "Right-to-left override"},
            {"input": "test\u202Badmin", "description": "Left-to-right override"},
            {"input": "test\u2067admin\u2067", "description": "Right-to-left isolate"},
            
            # Complex sequences
            {"input": "ᴮᴵᴳᴮᴵᴿᴰ", "description": "Spotify mathematical bold"},
            {"input": "＜script＞alert(1)＜/script＞", "description": "Fullwidth XSS"},
            {"input": "admin%uff07 UNION SELECT * FROM users --", "description": "URL-encoded fullwidth apostrophe"},
            
            # Edge cases
            {"input": "", "description": "Empty string"},
            {"input": "\u0000", "description": "Null character"},
            {"input": "\uFEFF", "description": "BOM only"},
            {"input": "a" * 1000, "description": "Long ASCII string"},
            {"input": "\u0301" * 50, "description": "Many combining marks"},
        ]
    
    def test_python_normalization(self):
        """Test Python's unicode normalization"""
        print("=== Python Normalization Test ===")
        
        python_results = []
        
        for test_case in self.test_cases:
            input_str = test_case["input"]
            description = test_case["description"]
            
            try:
                result = {
                    "input": input_str,
                    "description": description,
                    "nfc": unicodedata.normalize('NFC', input_str),
                    "nfd": unicodedata.normalize('NFD', input_str),
                    "nfkc": unicodedata.normalize('NFKC', input_str),
                    "nfkd": unicodedata.normalize('NFKD', input_str),
                    "input_code_points": [f"U+{ord(c):04X}" for c in input_str],
                    "input_bytes": input_str.encode('utf-8').hex(),
                    "error": None
                }
                
                # Check if forms differ
                result["forms_differ"] = len({result["nfc"], result["nfd"], result["nfkc"], result["nfkd"]}) > 1
                
                python_results.append(result)
                
            except Exception as e:
                python_results.append({
                    "input": input_str,
                    "description": description,
                    "error": str(e)
                })
        
        self.results["python"] = python_results
        return python_results
    
    def test_javascript_normalization(self):
        """Test JavaScript's String.prototype.normalize"""
        print("=== JavaScript Normalization Test ===")
        
        js_code = """
const testCases = JSON.parse(process.argv[1]);
const results = [];

for (const testCase of testCases) {
    try {
        const input = testCase.input;
        const result = {
            input: input,
            description: testCase.description,
            nfc: input.normalize('NFC'),
            nfd: input.normalize('NFD'),
            nfkc: input.normalize('NFKC'),
            nfkd: input.normalize('NFKD'),
            input_code_points: Array.from(input).map(c => 'U+' + c.charCodeAt(0).toString(16).toUpperCase().padStart(4, '0')),
            input_bytes: Buffer.from(input, 'utf8').toString('hex'),
            forms_differ: false,
            error: null
        };
        
        // Check if forms differ
        const forms = [result.nfc, result.nfd, result.nfkc, result.nfkd];
        result.forms_differ = new Set(forms).size > 1;
        
        results.push(result);
    } catch (error) {
        results.push({
            input: testCase.input,
            description: testCase.description,
            error: error.message
        });
    }
}

console.log(JSON.stringify(results));
"""
        
        try:
            # Run JavaScript test
            process = subprocess.run(
                ["node", "-e", js_code, json.dumps(self.test_cases)],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if process.returncode == 0:
                js_results = json.loads(process.stdout)
                self.results["javascript"] = js_results
                return js_results
            else:
                print(f"JavaScript test failed: {process.stderr}")
                return []
                
        except FileNotFoundError:
            print("Node.js not found, skipping JavaScript tests")
            return []
        except subprocess.TimeoutExpired:
            print("JavaScript test timed out")
            return []
        except Exception as e:
            print(f"JavaScript test error: {e}")
            return []
    
    def test_java_normalization(self):
        """Test Java's java.text.Normalizer"""
        print("=== Java Normalization Test ===")
        
        java_code = """
import java.text.Normalizer;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import com.google.gson.Gson;

public class NormalizationTest {
    public static class TestCase {
        public String input;
        public String description;
    }
    
    public static class Result {
        public String input;
        public String description;
        public String nfc;
        public String nfd;
        public String nfkc;
        public String nfkd;
        public List<String> input_code_points;
        public String input_bytes;
        public boolean forms_differ;
        public String error;
    }
    
    public static void main(String[] args) {
        Gson gson = new Gson();
        List<TestCase> testCases = gson.fromJson(args[0], 
            gson.fromJson("[]", List.class).getClass().getComponentType());
        
        List<Result> results = new ArrayList<>();
        
        for (TestCase testCase : testCases) {
            Result result = new Result();
            result.input = testCase.input;
            result.description = testCase.description;
            
            try {
                result.nfc = Normalizer.normalize(testCase.input, Normalizer.Form.NFC);
                result.nfd = Normalizer.normalize(testCase.input, Normalizer.Form.NFD);
                result.nfkc = Normalizer.normalize(testCase.input, Normalizer.Form.NFKC);
                result.nfkd = Normalizer.normalize(testCase.input, Normalizer.Form.NFKD);
                
                // Code points
                result.input_code_points = new ArrayList<>();
                for (int i = 0; i < testCase.input.length(); i++) {
                    int cp = testCase.input.codePointAt(i);
                    if (Character.isSupplementaryCodePoint(cp)) {
                        i++; // Skip surrogate pair second unit
                    }
                    result.input_code_points.add(String.format("U+%04X", cp));
                }
                
                // Bytes
                result.input_bytes = testCase.input.getBytes(StandardCharsets.UTF_8).toString();
                
                // Check if forms differ
                String[] forms = {result.nfc, result.nfd, result.nfkc, result.nfkd};
                result.forms_differ = java.util.Arrays.stream(forms).distinct().count() > 1;
                
                result.error = null;
            } catch (Exception e) {
                result.error = e.getMessage();
            }
            
            results.add(result);
        }
        
        System.out.println(gson.toJson(results));
    }
}
"""
        
        try:
            # Create temporary Java file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.java', delete=False) as f:
                f.write(java_code)
                java_file = f.name
            
            # Compile and run Java
            class_file = java_file.replace('.java', '.class')
            
            try:
                # Compile
                compile_process = subprocess.run(
                    ["javac", "-cp", ".", java_file],
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                
                if compile_process.returncode != 0:
                    print(f"Java compilation failed: {compile_process.stderr}")
                    return []
                
                # Run
                run_process = subprocess.run(
                    ["java", "-cp", ".", "NormalizationTest", json.dumps(self.test_cases)],
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                
                if run_process.returncode == 0:
                    java_results = json.loads(run_process.stdout)
                    self.results["java"] = java_results
                    return java_results
                else:
                    print(f"Java test failed: {run_process.stderr}")
                    return []
                    
            finally:
                # Clean up
                for file in [java_file, class_file]:
                    try:
                        os.unlink(file)
                    except:
                        pass
                        
        except FileNotFoundError:
            print("Java not found, skipping Java tests")
            return []
        except subprocess.TimeoutExpired:
            print("Java test timed out")
            return []
        except Exception as e:
            print(f"Java test error: {e}")
            return []
    
    def test_csharp_normalization(self):
        """Test C#'s string.Normalize"""
        print("=== C# Normalization Test ===")
        
        csharp_code = """
using System;
using System.Text;
using System.Globalization;
using System.Collections.Generic;
using Newtonsoft.Json;

public class TestCase {
    public string input { get; set; }
    public string description { get; set; }
}

public class Result {
    public string input { get; set; }
    public string description { get; set; }
    public string nfc { get; set; }
    public string nfd { get; set; }
    public string nfkc { get; set; }
    public string nfkd { get; set; }
    public List<string> input_code_points { get; set; }
    public string input_bytes { get; set; }
    public bool forms_differ { get; set; }
    public string error { get; set; }
}

public class Program {
    public static void Main(string[] args) {
        string jsonInput = args[0];
        List<TestCase> testCases = JsonConvert.DeserializeObject<List<TestCase>>(jsonInput);
        List<Result> results = new List<Result>();
        
        foreach (var testCase in testCases) {
            Result result = new Result();
            result.input = testCase.input;
            result.description = testCase.description;
            
            try {
                result.nfc = testCase.input.Normalize(NormalizationForm.FormC);
                result.nfd = testCase.input.Normalize(NormalizationForm.FormD);
                result.nfkc = testCase.input.Normalize(NormalizationForm.FormKC);
                result.nfkd = testCase.input.Normalize(NormalizationForm.FormKD);
                
                // Code points
                result.input_code_points = new List<string>();
                for (int i = 0; i < testCase.input.Length; i++) {
                    int cp = char.ConvertToUtf32(testCase.input, i);
                    result.input_code_points.Add($"U+{cp:X4}");
                    if (cp > 0xFFFF) i++; // Skip surrogate pair
                }
                
                // Bytes
                result.input_bytes = BitConverter.ToString(Encoding.UTF8.GetBytes(testCase.input)).Replace("-", "");
                
                // Check if forms differ
                string[] forms = { result.nfc, result.nfd, result.nfkc, result.nfkd };
                result.forms_differ = new HashSet<string>(forms).Count > 1;
                
                result.error = null;
            } catch (Exception e) {
                result.error = e.Message;
            }
            
            results.Add(result);
        }
        
        Console.WriteLine(JsonConvert.SerializeObject(results));
    }
}
"""
        
        try:
            # Create temporary C# file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.cs', delete=False) as f:
                f.write(csharp_code)
                cs_file = f.name
            
            try:
                # Compile and run C#
                compile_process = subprocess.run(
                    ["csc", "/reference:Newtonsoft.Json.dll", cs_file],
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                
                if compile_process.returncode != 0:
                    print(f"C# compilation failed: {compile_process.stderr}")
                    # Try without Newtonsoft.Json
                    simple_csharp = csharp_code.replace("Newtonsoft.Json.", "").replace("JsonConvert.", "System.Text.Json.")
                    with open(cs_file, 'w') as f:
                        f.write(simple_csharp)
                    
                    compile_process = subprocess.run(
                        ["csc", cs_file],
                        capture_output=True,
                        text=True,
                        timeout=30
                    )
                
                if compile_process.returncode != 0:
                    print(f"C# compilation failed: {compile_process.stderr}")
                    return []
                
                exe_file = cs_file.replace('.cs', '.exe')
                
                run_process = subprocess.run(
                    [exe_file, json.dumps(self.test_cases)],
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                
                if run_process.returncode == 0:
                    csharp_results = json.loads(run_process.stdout)
                    self.results["csharp"] = csharp_results
                    return csharp_results
                else:
                    print(f"C# test failed: {run_process.stderr}")
                    return []
                    
            finally:
                # Clean up
                for file in [cs_file, exe_file]:
                    try:
                        os.unlink(file)
                    except:
                        pass
                        
        except FileNotFoundError:
            print("C# compiler not found, skipping C# tests")
            return []
        except subprocess.TimeoutExpired:
            print("C# test timed out")
            return []
        except Exception as e:
            print(f"C# test error: {e}")
            return []
    
    def test_ruby_normalization(self):
        """Test Ruby's unicode normalization"""
        print("=== Ruby Normalization Test ===")
        
        ruby_code = """
require 'json'
require 'unicode_normalize'

test_cases = JSON.parse(ARGV[0])
results = []

test_cases.each do |test_case|
  begin
    input = test_case['input']
    
    result = {
      'input' => input,
      'description' => test_case['description'],
      'nfc' => input.unicode_normalize(:nfc),
      'nfd' => input.unicode_normalize(:nfd),
      'nfkc' => input.unicode_normalize(:nfkc),
      'nfkd' => input.unicode_normalize(:nfkd),
      'input_code_points' => input.codepoints.map { |cp| "U+%04X" % cp },
      'input_bytes' => input.encode('UTF-8').unpack('H*').first,
      'forms_differ' => false,
      'error' => nil
    }
    
    # Check if forms differ
    forms = [result['nfc'], result['nfd'], result['nfkc'], result['nfkd']]
    result['forms_differ'] = forms.uniq.length > 1
    
    results << result
  rescue => e
    results << {
      'input' => test_case['input'],
      'description' => test_case['description'],
      'error' => e.message
    }
  end
end

puts JSON.generate(results)
"""
        
        try:
            process = subprocess.run(
                ["ruby", "-e", ruby_code, json.dumps(self.test_cases)],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if process.returncode == 0:
                ruby_results = json.loads(process.stdout)
                self.results["ruby"] = ruby_results
                return ruby_results
            else:
                print(f"Ruby test failed: {process.stderr}")
                return []
                
        except FileNotFoundError:
            print("Ruby not found, skipping Ruby tests")
            return []
        except subprocess.TimeoutExpired:
            print("Ruby test timed out")
            return []
        except Exception as e:
            print(f"Ruby test error: {e}")
            return []
    
    def test_go_normalization(self):
        """Test Go's unicode normalization"""
        print("=== Go Normalization Test ===")
        
        go_code = """
package main

import (
    "encoding/json"
    "fmt"
    "unicode/utf8"
    "golang.org/x/text/unicode/norm"
)

type TestCase struct {
    Input        string `json:"input"`
    Description string `json:"description"`
}

type Result struct {
    Input          string   `json:"input"`
    Description    string   `json:"description"`
    NFC            string   `json:"nfc"`
    NFD            string   `json:"nfd"`
    NFKC           string   `json:"nfkc"`
    NFKD           string   `json:"nfkd"`
    InputCodePoints []string `json:"input_code_points"`
    InputBytes     string   `json:"input_bytes"`
    FormsDiffer    bool     `json:"forms_differ"`
    Error          string   `json:"error"`
}

func main() {
    var testCases []TestCase
    jsonInput := os.Args[1]
    if err := json.Unmarshal([]byte(jsonInput), &testCases); err != nil {
        fmt.Printf("Error parsing input: %v\\n", err)
        return
    }
    
    var results []Result
    
    for _, testCase := range testCases {
        result := Result{
            Input:       testCase.Input,
            Description: testCase.Description,
        }
        
        result.NFC = norm.NFC.String(testCase.Input)
        result.NFD = norm.NFD.String(testCase.Input)
        result.NFKC = norm.NFKC.String(testCase.Input)
        result.NFKD = norm.NFKD.String(testCase.Input)
        
        // Code points
        for i, r := range testCase.Input {
            cp := r
            if cp > 0xFFFF {
                // Handle surrogate pairs if needed
                cp = r
            }
            result.InputCodePoints = append(result.InputCodePoints, fmt.Sprintf("U+%04X", cp))
        }
        
        // Bytes
        result.InputBytes = fmt.Sprintf("%x", []byte(testCase.Input))
        
        // Check if forms differ
        forms := []string{result.NFC, result.NFD, result.NFKC, result.NFKD}
        formSet := make(map[string]bool)
        for _, form := range forms {
            formSet[form] = true
        }
        result.FormsDiffer = len(formSet) > 1
        
        jsonResult, _ := json.Marshal(result)
        results = append(results, result)
        fmt.Println(string(jsonResult))
    }
}
"""
        
        try:
            # Create temporary Go file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.go', delete=False) as f:
                f.write(go_code)
                go_file = f.name
            
            try:
                # Initialize Go module and run
                subprocess.run(["go", "mod", "init", "test"], 
                           cwd=os.path.dirname(go_file), 
                           capture_output=True)
                subprocess.run(["go", "get", "golang.org/x/text/unicode/norm"], 
                           cwd=os.path.dirname(go_file), 
                           capture_output=True)
                
                process = subprocess.run(
                    ["go", "run", go_file, json.dumps(self.test_cases)],
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                
                if process.returncode == 0:
                    # Parse line-by-line JSON output
                    go_results = []
                    for line in process.stdout.strip().split('\n'):
                        if line.strip():
                            go_results.append(json.loads(line))
                    
                    self.results["go"] = go_results
                    return go_results
                else:
                    print(f"Go test failed: {process.stderr}")
                    return []
                    
            finally:
                # Clean up
                try:
                    os.unlink(go_file)
                except:
                    pass
                        
        except FileNotFoundError:
            print("Go not found, skipping Go tests")
            return []
        except subprocess.TimeoutExpired:
            print("Go test timed out")
            return []
        except Exception as e:
            print(f"Go test error: {e}")
            return []
    
    def compare_results(self):
        """Compare results across different languages"""
        print("\n=== Cross-Language Comparison ===")
        
        languages = list(self.results.keys())
        if len(languages) < 2:
            print("Need at least 2 languages for comparison")
            return
        
        inconsistencies = []
        
        for i, test_case in enumerate(self.test_cases):
            input_str = test_case["input"]
            description = test_case["description"]
            
            # Collect results for this test case
            case_results = {}
            for lang, results in self.results.items():
                if i < len(results):
                    result = results[i]
                    if not result.get("error"):
                        case_results[lang] = result
            
            # Check for inconsistencies
            if len(case_results) > 1:
                # Check NFC consistency
                nfc_values = {lang: result["nfc"] for lang, result in case_results.items()}
                if len(set(nfc_values.values())) > 1:
                    inconsistencies.append({
                        "input": input_str,
                        "description": description,
                        "type": "NFC inconsistency",
                        "values": nfc_values
                    })
                
                # Check NFD consistency
                nfd_values = {lang: result["nfd"] for lang, result in case_results.items()}
                if len(set(nfd_values.values())) > 1:
                    inconsistencies.append({
                        "input": input_str,
                        "description": description,
                        "type": "NFD inconsistency",
                        "values": nfd_values
                    })
                
                # Check NFKC consistency
                nfkc_values = {lang: result["nfkc"] for lang, result in case_results.items()}
                if len(set(nfkc_values.values())) > 1:
                    inconsistencies.append({
                        "input": input_str,
                        "description": description,
                        "type": "NFKC inconsistency",
                        "values": nfkc_values
                    })
                
                # Check NFKD consistency
                nfkd_values = {lang: result["nfkd"] for lang, result in case_results.items()}
                if len(set(nfkd_values.values())) > 1:
                    inconsistencies.append({
                        "input": input_str,
                        "description": description,
                        "type": "NFKD inconsistency",
                        "values": nfkd_values
                    })
        
        # Report inconsistencies
        if inconsistencies:
            print(f"\n🚨 Found {len(inconsistencies)} cross-language inconsistencies:")
            for inconsistency in inconsistencies[:10]:  # Show first 10
                print(f"\nInput: {inconsistency['input']}")
                print(f"Description: {inconsistency['description']}")
                print(f"Type: {inconsistency['type']}")
                print("Values:")
                for lang, value in inconsistency['values'].items():
                    print(f"  {lang}: {value}")
        else:
            print("\n✅ No cross-language inconsistencies found")
        
        return inconsistencies
    
    def generate_security_report(self):
        """Generate security-focused report"""
        print("\n=== Security Analysis Report ===")
        
        security_issues = []
        
        for lang, results in self.results.items():
            for result in results:
                if result.get("error"):
                    continue
                
                input_str = result["input"]
                
                # Check for dangerous normalization patterns
                if result["forms_differ"]:
                    # Check if NFKC introduces dangerous characters
                    nfkc = result["nfkc"]
                    dangerous_chars = ["'", '"', ';', '|', '&', '`', '$', '(', ')', '<', '>', '/', '\\']
                    
                    for char in dangerous_chars:
                        if char in nfkc and char not in input_str:
                            security_issues.append({
                                "language": lang,
                                "input": input_str,
                                "description": result.get("description", ""),
                                "issue": f"NFKC introduces dangerous character '{char}'",
                                "normalized": nfkc,
                                "severity": "HIGH"
                            })
                    
                    # Check for path traversal
                    if ".." in nfkc and ".." not in input_str:
                        security_issues.append({
                            "language": lang,
                            "input": input_str,
                            "description": result.get("description", ""),
                            "issue": "NFKC introduces path traversal sequence '..'",
                            "normalized": nfkc,
                            "severity": "HIGH"
                        })
                    
                    # Check for HTML tags
                    if "<" in nfkc and ">" in nfkc and ("<" not in input_str or ">" not in input_str):
                        security_issues.append({
                            "language": lang,
                            "input": input_str,
                            "description": result.get("description", ""),
                            "issue": "NFKC introduces HTML tag characters",
                            "normalized": nfkc,
                            "severity": "MEDIUM"
                        })
        
        # Report security issues
        if security_issues:
            print(f"\n🚨 Found {len(security_issues)} potential security issues:")
            
            # Group by severity
            high_issues = [i for i in security_issues if i["severity"] == "HIGH"]
            medium_issues = [i for i in security_issues if i["severity"] == "MEDIUM"]
            
            if high_issues:
                print(f"\n🔴 HIGH SEVERITY ({len(high_issues)}):")
                for issue in high_issues[:5]:
                    print(f"  {issue['language']}: {issue['issue']}")
                    print(f"    Input: {issue['input']}")
                    print(f"    Normalized: {issue['normalized']}")
            
            if medium_issues:
                print(f"\n🟡 MEDIUM SEVERITY ({len(medium_issues)}):")
                for issue in medium_issues[:5]:
                    print(f"  {issue['language']}: {issue['issue']}")
                    print(f"    Input: {issue['input']}")
                    print(f"    Normalized: {issue['normalized']}")
        else:
            print("\n✅ No obvious security issues found")
        
        return security_issues
    
    def save_results(self, filename="multi_language_normalization_results.json"):
        """Save all results to JSON file"""
        output = {
            "metadata": {
                "timestamp": "2025-04-06",
                "languages_tested": list(self.results.keys()),
                "total_test_cases": len(self.test_cases),
                "description": "Multi-language Unicode normalization security analysis"
            },
            "test_cases": self.test_cases,
            "results": self.results,
            "inconsistencies": self.compare_results(),
            "security_issues": self.generate_security_report()
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        
        print(f"\n📄 Results saved to {filename}")
        return filename
    
    def run_all_tests(self):
        """Run normalization tests for all available languages"""
        print("🧪 Starting Multi-Language Unicode Normalization Tests")
        print(f"Testing {len(self.test_cases)} cases across multiple languages...\n")
        
        # Test each language
        languages_to_test = [
            ("python", self.test_python_normalization),
            ("javascript", self.test_javascript_normalization),
            ("java", self.test_java_normalization),
            ("csharp", self.test_csharp_normalization),
            ("ruby", self.test_ruby_normalization),
            ("go", self.test_go_normalization),
        ]
        
        for lang_name, test_func in languages_to_test:
            try:
                test_func()
                print(f"✅ {lang_name.title()} tests completed")
            except Exception as e:
                print(f"❌ {lang_name.title()} tests failed: {e}")
        
        # Generate reports
        self.compare_results()
        self.generate_security_report()
        
        # Save results
        return self.save_results()

def main():
    """Main function to run the multi-language normalization test suite"""
    tester = MultiLanguageNormalizationTester()
    
    # Run all tests
    results_file = tester.run_all_tests()
    
    print(f"\n🎉 Multi-language normalization testing complete!")
    print(f"Results saved to: {results_file}")
    print(f"Languages tested: {', '.join(tester.results.keys())}")
    
    # Show summary statistics
    total_tests = len(tester.test_cases) * len(tester.results)
    print(f"Total tests run: {total_tests}")

if __name__ == "__main__":
    main()
