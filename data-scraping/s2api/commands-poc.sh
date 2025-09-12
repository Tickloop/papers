#!/bin/bash
start_date=$(curl https://api.semanticscholar.org/datasets/v1/release/ -sS | jq ".[-2]" | tr -d '"')
end_date=$(curl https://api.semanticscholar.org/datasets/v1/release/ -sS | jq ".[-1]" | tr -d '"')
api_key=$S2_API_KEY

if [[ $api_key == "" ]]; then
    echo -e "\033[31mS2 API Key env variable missing. Please set S2_API_KEY\033[0m"
    exit 1
fi

function download_diff() {
    local dataset=$1

    echo -e "\033[32mDownloading $dataset diffs from $start_date to $end_date...\033[0m"

    curl -H "x-api-key: $api_key" \
        --url "https://api.semanticscholar.org/datasets/v1/diffs/$start_date/to/$end_date/$dataset" \
        | jq ".diffs[0].update_files[0]" \
        | tr -d '"' \
        | xargs curl -sS --output "./$dataset.gz"

    sleep 1
}

function print_file_info() {
    local file=$1
    if [ -f "$file" ]; then
        local size=$(du -h "$file" | cut -f1)
        local lines=$(zcat "$file" | wc -l)
        echo -e "\033[34mDownloaded $file: Size = $size, Lines = $lines\033[0m"
    else
        echo -e "\033[31mFile $file does not exist.\033[0m"
    fi
}


download_diff "tldrs"
print_file_info "./tldrs.gz"
gzip -d ./tldrs.gz


download_diff "abstracts"
print_file_info "./abstracts.gz"
gzip -d ./abstracts.gz


download_diff "papers"
print_file_info "./papers.gz"
gzip -d ./papers.gz


echo -e "\033[32mAll downloads completed.\033[0m"