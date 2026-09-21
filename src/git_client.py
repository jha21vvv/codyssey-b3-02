                                                        
                                              
"""
# [1차]: Git 상태 및 변경 사항(diff)을 수집하는 클라이언트 모듈임을 정의합니다.
# [2차]: 개발자가 코드를 고치고 나면 "어디를 얼마나 고쳤니?" 하고 Git에게 물어봐 주는 척척박사입니다.
Git 상태 및 변경 사항(diff)을 수집하는 클라이언트 모듈
# [1차]: 모듈 독스트링을 닫는 삼중 따옴표입니다.
# [2차]: 설명 팻말을 닫습니다.
"""

                                                     
                                                  
import os
                                                                         
                                                                 
import subprocess
                                                           
                                                          
from typing import List, Optional


                                                                      
                                             
def run_git_command(args: List[str], cwd: Optional[str] = None) -> subprocess.CompletedProcess:
                                         
                      
    """Git 명령을 실행하고 완료된 프로세스 객체를 반환합니다."""
                                                                               
                                                                                   
    working_dir = cwd or os.getcwd()
                                                                              
                                                          
    return subprocess.run(
                                                                                                       
                                                                                           
        # 마이: -c"이번 한 번만 임시로 설정 바꿔줘!"  core Git의 설정 카테고리 중 '기본 시스템' 영역  
                                                                                      
        ["git", "-c", "core.quotepath=false"] + args,
                                            
                                                           
        cwd=working_dir,
                                                                         
                                                          
        capture_output=True,
                                                             
                                                                       
        text=True,
                                                                  
                                                                         
        encoding="utf-8",
                                                                           
                                                                                  
        errors="replace"
                                       
                      
    )


                                                                
                                                            
def is_git_repository(cwd: Optional[str] = None) -> bool:
                                     
                      
    """현재 디렉토리가 Git 저장소 루트 또는 내부에 위치하는지 확인합니다."""
                                                                                 
                                                                          
    result = run_git_command(["rev-parse", "--is-inside-work-tree"], cwd=cwd)
                                                              
                                                                                        
    return result.returncode == 0 and result.stdout.strip() == "true"


                                                  
                                                            
def get_git_root(cwd: Optional[str] = None) -> Optional[str]:
                                     
                      
    """Git 저장소의 최상위 루트 디렉토리 경로를 반환합니다."""
                                                                    
                                                      
    # 마이: 깃에서 변동사항등을 체크할때 제일위에서해야 전부 반영되니 만든것
    result = run_git_command(["rev-parse", "--show-toplevel"], cwd=cwd)
                                                       
                                  
    if result.returncode == 0:
                                                 
                                                            
        #마이: stdout 터미널 까만 화면에 정상적으로 찍힌 글자 텍스트
        return result.stdout.strip()
                                              
                                                        
    return None


                                                                      
                                                          
def get_changed_files(cwd: Optional[str] = None) -> List[str]:
                                          
                    
    """
    # [1차]: git status --porcelain 결과를 기계적으로 파싱하여 변경된 파일 목록을 추출함을 기술합니다.
    # [2차]: 사람이 보기 좋은 문구 대신 컴퓨터가 읽기 좋게 규격화된 상태 표를 읽어온다고 설명합니다.
    git status --porcelain 결과를 파싱하여 변경, 추가, 삭제된 파일 목록을 반환합니다.
    # [1차]: Docstring을 닫습니다.
    # [2차]: 설명서 닫기.
    """
                                             
                                                                  
    result = run_git_command(["status", "--porcelain"], cwd=cwd)
                                                            
                                                                     
    if result.returncode != 0:
        return []

                                                
                                         
    changed_files = []
                                                                
                                                    
    for line in result.stdout.splitlines():
                                      
                                 
        trimmed = line.strip()
                                                   
                                               
        if not trimmed:
            continue
                                                                        
                                                                                        
        parts = line[3:].strip()
                                                               
                                     
        if " -> " in parts:
                                                                 
                                                           
            parts = parts.split(" -> ")[1].strip()
                                                      
                                                   
        if parts.startswith('"') and parts.endswith('"'):
                                                         
                                          
            parts = parts[1:-1]
                                                
                                      
        if parts:
                                                          
                                             
            changed_files.append(parts)

                                          
                                   
    return changed_files


                                                   
                                                             
def get_git_diff(staged_only: bool = False, cwd: Optional[str] = None) -> str:
                                                                   
                   
    """
    # [1차]: diff 수집 규칙(staged 우선 조회 및 unstaged 결합)을 기술합니다.
    # [2차]: staged만 볼 것인지, 파일 수정한 것 전체를 다 볼 것인지 옵션 안내입니다.
    git diff 결과를 수집합니다.
    - staged_only=True: git diff --cached (스테이징된 변경사항)
    - staged_only=False: staged 및 unstaged 변경사항을 모두 수집 (staged 우선 및 결합)
    # [1차]: Docstring을 닫습니다.
    # [2차]: 설명서 끝.
    """
                                                  
                                                          
    if staged_only:
                                                             
                                                         
        res_staged = run_git_command(["diff", "--cached"], cwd=cwd)
                                                    
                                                        
        return res_staged.stdout if res_staged.returncode == 0 else ""

                                                            
                                                    
    res_staged = run_git_command(["diff", "--cached"], cwd=cwd)
                                                     
                           
    staged_diff = res_staged.stdout if res_staged.returncode == 0 else ""

                                                        
                                                              
    res_unstaged = run_git_command(["diff"], cwd=cwd)
                                                         
                           
    unstaged_diff = res_unstaged.stdout if res_unstaged.returncode == 0 else ""

                                              
                                   
    diffs = []
                                             
                                        
    if staged_diff.strip():
                                                   
                                  
        diffs.append(staged_diff.strip())
                                                       
                                         
    if unstaged_diff.strip():
                                                     
                                  
        diffs.append(unstaged_diff.strip())

                                                            
                                                                            
    return "\n\n".join(diffs)


                                                                  
                                                            
def has_changes(cwd: Optional[str] = None) -> bool:
                                      
                   
    """
    # [1차]: 변경 사항(수정된 파일 또는 diff 내용)이 존재하는지 확인함을 기술합니다.
    # [2차]: 변경점이 하나라도 있는지 체크한다는 설명입니다.
    변경 사항(수정된 파일 또는 diff 내용)이 존재하는지 확인합니다.
    # [1차]: Docstring을 닫습니다.
    # [2차]: 설명서 닫기.
    """
                             
                            
    files = get_changed_files(cwd=cwd)
                                  
                             
    diff = get_git_diff(cwd=cwd)
                                                                   
                                                                                                              
    return bool(files or diff.strip())
