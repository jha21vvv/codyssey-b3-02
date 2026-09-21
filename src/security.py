                                                     
                                                                                
"""
# [1차]: 민감 정보 마스킹 및 diff 길이/파일 수 제한을 처리하는 모듈(--safe-mode)임을 명시합니다.
# [2차]: API 키 유출로 몇 백만 원 요금 폭탄을 맞지 않도록 사전에 지켜주는 안전 금고 역할을 설명합니다.
민감 정보 마스킹 및 diff 길이/파일 수 제한을 처리하는 보안 모듈 (--safe-mode)
# [1차]: 모듈 독스트링을 닫는 삼중 따옴표입니다.
# [2차]: 팻말 닫기.
"""

                                                       
                                                                          
import re
                                                     
                                                   
from typing import List, Tuple

                                                        
                                                           
SENSITIVE_PATTERNS = [
                                                                                              
                                                                
    # 마이: 나중에 검색하기 좋도록 문자열 형식을 다듬어둬서 그에 맞는 문자열을 빠르게 찾으려는것
    (re.compile(r"-----BEGIN (?:[A-Z ]+)?PRIVATE KEY-----[\s\S]*?-----END (?:[A-Z ]+)?PRIVATE KEY-----"), "[REDACTED_PRIVATE_KEY]"),
                                                                                  
                                                                                         
    (re.compile(r"\bsk-[a-zA-Z0-9]{20,}\b"), "[REDACTED_API_KEY]"),
                                                                                        
                                             
    (re.compile(r"\bsk-ant-[a-zA-Z0-9_\-]{20,}\b"), "[REDACTED_API_KEY]"),
                                                                                                       
                                                          
    (re.compile(r"\b(?:ghp|gho|ghu|ghs|ghr)_[a-zA-Z0-9]{36,}\b"), "[REDACTED_GITHUB_TOKEN]"),
                                                                                       
                                                     
    (re.compile(r"\bAKIA[0-9A-Z]{16}\b"), "[REDACTED_AWS_KEY]"),
                                                                          
                                                      
    (re.compile(r"\b[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}\b"), "[REDACTED_EMAIL]"),
                                                                                                     
                                                                                                                 
    (re.compile(r'(?i)(["\']?(?:api[_\-]?key|secret|token|password|auth[_\-]?token)["\']?\s*[:=]\s*["\'])(?!\[REDACTED_)([^"\']{4,})(["\'])'), r"\1[REDACTED_SECRET]\3"),
                                        
                    
]


                                                             
                                                         
def mask_sensitive_data(text: str) -> str:
                                          
                   
    """
    # [1차]: 텍스트 내 API 키, 비밀번호 등을 감지하여 안전하게 치환함을 기술합니다.
    # [2차]: 설명입니다.
    텍스트 내에 포함된 민감 정보(API 키, 토큰, 비밀번호, 이메일 등)를 감지하여 마스킹합니다.
    # [1차]: Docstring을 닫습니다.
    # [2차]: 설명서 끝.
    """
                                                      
                                            
    if not text:
        return text

                                                         
                                    
    masked = text
                                                             
                                                               
    for pattern, replacement in SENSITIVE_PATTERNS:
                                                              
                                                  
        # 마이: 패턴에 해당되는 형식이 마스크에서 발견되면 리플레이스로 바꾸는 구조.
        masked = pattern.sub(replacement, masked)

                                          
                                      
    return masked


                                                                      
                                                                           
def truncate_diff(diff_text: str, max_files: int = 10, max_lines: int = 200) -> str:
                                                 
                   
    """
    # [1차]: 파일 수(기본 10개) 및 줄 수(기본 200줄) 제한 규칙을 기술합니다.
    # [2차]: 자르는 기준 한도 설명입니다.
    diff 텍스트의 크기를 제한합니다.
    - 최대 파일 수(max_files, 기본 10개) 초과 시 절삭
    - 최대 라인 수(max_lines, 기본 200줄) 초과 시 절삭
    # [1차]: Docstring을 닫습니다.
    # [2차]: 설명서 끝.
    """
                                   
                                  
    if not diff_text:
        return ""

                                           
                                      
    lines = diff_text.splitlines()

                                                                     
                                                      
    file_indices: List[int] = []
                                       
                                             
    for idx, line in enumerate(lines):
                                                                    
                                                         
        if line.startswith("diff --git "):
                                             
                                     
            file_indices.append(idx)

                                     
                                        
    total_files = len(file_indices)
                                              
                                             
    file_truncated = False
                                         
                                    
    files_omitted = 0

                                                         
                                           
    if total_files > max_files:
                                                                    
                                                             
        cutoff_line = file_indices[max_files]
                                 
                                                    
        files_omitted = total_files - max_files
                                                         
                                             
        lines = lines[:cutoff_line]
                                       
                                       
        file_truncated = True

                                        
                                                      
    total_lines = len(lines)
                                     
                            
    line_truncated = False
                                                        
                                        
    if total_lines > max_lines:
                                                  
                                      
        lines = lines[:max_lines]
                                       
                                      
        line_truncated = True

                                            
                                            
    result = "\n".join(lines)

                                      
                                                         
    notices = []
                                           
                                                            
    if file_truncated:
        notices.append(f"... [diff truncated by safe-mode: 최대 {max_files}개 파일 초과 (외 {files_omitted}개 파일 생략)]")
                                           
                                                            
    if line_truncated:
        notices.append(f"... [diff truncated by safe-mode: 최대 {max_lines}줄 초과 (전체 {total_lines}줄 중 {max_lines}줄만 전송)]")

                                              
                                       
    if notices:
        result += "\n\n" + "\n".join(notices)

                                          
                                                
    return result


                                                                        
                                                                            
def apply_safe_mode(
    diff_text: str,
    enabled: bool = True,
    max_files: int = 10,
    max_lines: int = 200
) -> str:
                                              
                   
    """
    # [1차]: enabled가 True일 때 마스킹과 크기 절삭을 차례로 적용함을 기술합니다.
    # [2차]: 원스톱 보안 처리 안내입니다.
    --safe-mode 파이프라인을 실행합니다.
    enabled가 True일 때 민감정보 마스킹 및 파일/라인 절삭을 차례로 적용합니다.
    # [1차]: Docstring을 닫습니다.
    # [2차]: 설명서 끝.
    """
                                                              
                                                               
    if not enabled or not diff_text:
        return diff_text

                                                       
                                              
    masked = mask_sensitive_data(diff_text)
                                                      
                                                     
    truncated = truncate_diff(masked, max_files=max_files, max_lines=max_lines)

                                           
                                                     
    return truncated
