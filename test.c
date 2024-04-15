#include<stdio.h>

int contains(int * test, int val, int size){
    for(int i =0; i<size; i++){
        if(test[i]==val){
            return 1;
        }
    }
    return 0;
}

int removeDuplicates(int* nums, int numsSize) {
    // int temp[numsSize];
    // int j=0;
    // for (int i =0; i<numsSize; i++){
    //     if (!contains(temp, nums[i], numsSize)){
    //         temp[j++] = nums[i];
    //     }
    // }
    // return j+1;
    int j = 1;
    for(int i = 1; i < numsSize; i++){
        if(nums[i] != nums[i - 1]){
            nums[j] = nums[i];
            j++;
        }
    }
    return j;
}

int main(){
    int arr[13]= {0,0,1,1,1,5, 5, 6, 2,2,3,3,4};
    printf("number of unique elements are %d", removeDuplicates(arr, 13));
}