import React, { useState, useEffect } from "react";

function StatusMessage({ message = "" }) {
  const [displayedText, setDisplayedText] = useState(""); // 초기 상태 설정
  const typingSpeed = 80; // 타이핑 속도 (밀리초)

  useEffect(() => {
    // message가 유효하지 않을 경우 초기화
    if (!message || typeof message !== "string") {
      return;
    }

    // 초기화
    setDisplayedText(""); // 상태 초기화
    let currentIndex = 0; // 현재 타이핑 중인 문자 인덱스

    // 타이핑 효과 구현
    const typingEffect = setInterval(() => {
      if (currentIndex < message.length) {
        const nextChar = message[currentIndex];
        if (nextChar === "(") setDisplayedText((prev) => prev + "\n" + nextChar); // 줄바꿈 후 괄호 추가
        else setDisplayedText((prev) => prev + nextChar); // 그냥 문자 추가
        currentIndex++;
      } else {
        clearInterval(typingEffect); // 타이핑 완료 시 타이머 정리
      }
    }, typingSpeed);

    // message 변경 시 또는 컴포넌트 언마운트 시 클리너 실행
    return () => {
      clearInterval(typingEffect);
    };
  }, [message]); // message가 변경될 때마다 실행

  return (
    <h1 className="typing-effect">
      {displayedText} {/* 상태로 업데이트된 텍스트 표시 */}
    </h1>
  );
}

export default StatusMessage;
