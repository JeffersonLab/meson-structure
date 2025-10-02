#!/bin/bash
# Quick fix for Snakemake pulp issue and test setup

echo "======================================"
echo "Fixing Snakemake pulp issue"
echo "======================================"

# Try to fix the pulp issue
echo -e "\nAttempting to fix pulp compatibility issue..."

# Option 1: Try uninstalling pulp first (safest)
echo "Trying: pip uninstall pulp..."
pip uninstall -y pulp 2>/dev/null

# Test if it works now
echo -e "\nTesting Snakemake..."
if snakemake --version > /dev/null 2>&1; then
    echo "✓ Snakemake is working! Version: $(snakemake --version)"
else
    echo "Still not working, trying to downgrade pulp..."
    pip install 'pulp<2.8' 2>/dev/null
    
    if snakemake --version > /dev/null 2>&1; then
        echo "✓ Fixed by downgrading pulp. Snakemake version: $(snakemake --version)"
    else
        echo "✗ Still having issues. You may need to reinstall Snakemake"
        echo "  Try: pip install --upgrade --force-reinstall snakemake"
        exit 1
    fi
fi

echo -e "\n======================================"
echo "Testing Pipeline Setup"
echo "======================================"

# Test the pipeline
echo -e "\n1. Checking files..."
[ -f "Snakefile.smk" ] && echo "✓ Snakefile.smk found" || echo "✗ Snakefile.smk not found"
[ -f "config.yaml" ] && echo "✓ config.yaml found" || echo "✗ config.yaml not found"

echo -e "\n2. Testing list_hepmc rule..."
snakemake -s Snakefile.smk list_hepmc 2>&1 | head -20

echo -e "\n======================================"
echo "Setup complete!"
echo "======================================"
echo ""
echo "Next steps:"
echo "1. Review the HEPMC file counts above"
echo "2. Test job creation: snakemake -s Snakefile.smk create_only -j 4"
echo "3. Submit jobs: snakemake -s Snakefile.smk submit_only -j 4"
