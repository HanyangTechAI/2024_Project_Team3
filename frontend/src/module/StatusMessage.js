import React, { useState, useEffect } from 'react';

function StatusMessage({ message = '' }) {
  const [displayedText, setDisplayedText] = useState(''); // 초기값 설정
  const typingSpeed = 100; // 타이핑 속도 (밀리초)

  useEffect(() => {
    // 메시지가 비어있으면 초기화
    if (!message) {
      setDisplayedText('');
      return "";
    }


    setDisplayedText(''); // 이전 메시지를 초기화
    let currentIndex = 0;

    // 타이핑 효과 구현
    const typingEffect = setInterval(() => {
      if (currentIndex < message.length) {
        setDisplayedText((prev) => prev + message[currentIndex]);
        currentIndex++;
      } else {
        //clearInterval(typingEffect); // 애니메이션 완료 시 정지
      }
    }, typingSpeed);

    // 컴포넌트 언마운트 또는 메시지 변경 시 인터벌 정리
    return () => {
      clearInterval(typingEffect);
    };
  }, [message]); // message가 변경될 때마다 실행

  return <h1 className="typing-effect">{displayedText}</h1>;
}

export default StatusMessage;
