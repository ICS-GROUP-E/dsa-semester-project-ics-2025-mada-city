#!/usr/bin/env python3
"""
Test runner for the DSA Student Management System
"""
import sys
import os
import subprocess


def run_test(test_file):
    """Run a single test file."""
    print(f"\n🧪 Running {test_file}...")
    print("-" * 50)

    try:
        result = subprocess.run(
            [sys.executable, f"dsaproject/test/{test_file}"],
            capture_output=True,
            text=True,
            cwd=os.path.dirname(os.path.abspath(__file__))
        )

        if result.returncode == 0:
            print(f"✅ {test_file} PASSED")
            if result.stdout:
                print(result.stdout)
        else:
            print(f"❌ {test_file} FAILED")
            if result.stderr:
                print(f"Error: {result.stderr}")
            if result.stdout:
                print(f"Output: {result.stdout}")

        return result.returncode == 0
    except Exception as e:
        print(f"❌ Error running {test_file}: {e}")
        return False


def main():
    """Run all tests."""
    print("🎯 DSA Student Management System - Test Suite")
    print("=" * 60)

    # List of test files
    test_files = [
        "test_bst.py",
        "test_linkedlist.py",
        "test_stack.py",
        "test_queue.py",
        "test_student_service.py"
    ]

    results = []

    for test_file in test_files:
        passed = run_test(test_file)
        results.append((test_file, passed))

    # Summary
    print("\n" + "=" * 60)
    print("📊 Test Results Summary:")
    print("-" * 60)

    passed_count = 0
    for test_file, passed in results:
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{test_file:<25} {status}")
        if passed:
            passed_count += 1

    print("-" * 60)
    print(f"Total: {passed_count}/{len(test_files)} tests passed")

    if passed_count == len(test_files):
        print("\n🎉 All tests passed! System is working correctly.")
        print("🚀 Ready to run 'python main.py' for the GUI application!")
    else:
        print(f"\n⚠️  {len(test_files) - passed_count} test(s) failed. Please check the errors above.")

    return passed_count == len(test_files)


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

