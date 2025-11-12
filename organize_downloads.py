import os
import shutil
from pathlib import Path

# 다운로드 폴더 경로
DOWNLOADS_FOLDER = r"C:\Users\student\Downloads"

# 파일 분류 규칙: {대상폴더: [파일확장자들]}
FILE_CATEGORIES = {
    "images": [".jpg", ".jpeg"],
    "data": [".csv", ".xlsx"],
    "docs": [".txt", ".doc", ".pdf"],
    "archive": [".zip"]
}


def create_folders_if_not_exist():
    """대상 폴더들이 없으면 생성"""
    for folder_name in FILE_CATEGORIES.keys():
        folder_path = os.path.join(DOWNLOADS_FOLDER, folder_name)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            print(f"폴더 생성: {folder_path}")
        else:
            print(f"폴더 존재: {folder_path}")


def organize_files():
    """다운로드 폴더의 파일들을 분류하여 이동"""
    if not os.path.exists(DOWNLOADS_FOLDER):
        print(f"오류: 다운로드 폴더를 찾을 수 없습니다: {DOWNLOADS_FOLDER}")
        return
    
    # 다운로드 폴더의 모든 파일 확인
    files_moved = 0
    files_skipped = 0
    
    for filename in os.listdir(DOWNLOADS_FOLDER):
        file_path = os.path.join(DOWNLOADS_FOLDER, filename)
        
        # 디렉토리는 스킵 (이미 생성된 폴더들)
        if os.path.isdir(file_path):
            continue
        
        # 파일의 확장자 확인
        file_extension = Path(filename).suffix.lower()
        
        # 해당하는 폴더 찾기
        target_folder = None
        for folder_name, extensions in FILE_CATEGORIES.items():
            if file_extension in extensions:
                target_folder = folder_name
                break
        
        # 분류된 폴더가 있으면 이동
        if target_folder:
            target_path = os.path.join(DOWNLOADS_FOLDER, target_folder, filename)
            try:
                shutil.move(file_path, target_path)
                print(f"이동됨: {filename} → {target_folder}/")
                files_moved += 1
            except Exception as e:
                print(f"오류 - {filename} 이동 실패: {str(e)}")
        else:
            # 지정된 분류에 없는 파일은 스킵
            files_skipped += 1
    
    print(f"\n정리 완료!")
    print(f"이동된 파일: {files_moved}개")
    print(f"분류 미대상 파일: {files_skipped}개")


if __name__ == "__main__":
    print("=== 다운로드 폴더 정리 시작 ===\n")
    
    # 1단계: 필요한 폴더 생성
    print("[1단계] 필요한 폴더 생성...")
    create_folders_if_not_exist()
    
    print("\n[2단계] 파일 이동 중...\n")
    # 2단계: 파일 이동
    organize_files()
