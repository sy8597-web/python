/* ========================
   네비게이션 스크롤 함수
   ======================== */

function scrollToSection(sectionId) {
    const element = document.getElementById(sectionId);
    if (element) {
        element.scrollIntoView({ behavior: 'smooth' });
    }
}

/* ========================
   계산기 기능
   ======================== */

function calculate() {
    const num1 = parseFloat(document.getElementById('num1').value);
    const num2 = parseFloat(document.getElementById('num2').value);
    const operator = document.getElementById('operator').value;
    const resultDiv = document.getElementById('result');

    // 입력값 검증
    if (isNaN(num1) || isNaN(num2)) {
        resultDiv.textContent = '⚠️ 숫자를 입력해주세요!';
        resultDiv.style.color = '#e74c3c';
        return;
    }

    let result;
    switch (operator) {
        case '+':
            result = num1 + num2;
            break;
        case '-':
            result = num1 - num2;
            break;
        case '*':
            result = num1 * num2;
            break;
        case '/':
            if (num2 === 0) {
                resultDiv.textContent = '⚠️ 0으로 나눌 수 없습니다!';
                resultDiv.style.color = '#e74c3c';
                return;
            }
            result = num1 / num2;
            break;
        default:
            result = 0;
    }

    // 결과 표시
    resultDiv.textContent = `${num1} ${operator} ${num2} = ${result.toFixed(2)}`;
    resultDiv.classList.add('show');
    resultDiv.style.color = '#27ae60';

    // 애니메이션 리셋
    setTimeout(() => {
        resultDiv.classList.remove('show');
    }, 3000);
}

// Enter 키로 계산
document.addEventListener('DOMContentLoaded', function() {
    const num2Input = document.getElementById('num2');
    if (num2Input) {
        num2Input.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                calculate();
            }
        });
    }
});

/* ========================
   색상 변환기 기능
   ======================== */

function changeBackgroundColor() {
    const colorPicker = document.getElementById('colorPicker');
    const colorCode = document.getElementById('colorCode');
    const selectedColor = colorPicker.value;

    // 배경색 변경
    document.body.style.backgroundColor = selectedColor;
    colorCode.textContent = `현재 색상: ${selectedColor.toUpperCase()}`;
}

function randomColor() {
    const letters = '0123456789ABCDEF';
    let color = '#';

    for (let i = 0; i < 6; i++) {
        color += letters[Math.floor(Math.random() * 16)];
    }

    const colorPicker = document.getElementById('colorPicker');
    const colorCode = document.getElementById('colorCode');

    colorPicker.value = color;
    document.body.style.backgroundColor = color;
    colorCode.textContent = `현재 색상: ${color.toUpperCase()}`;

    // 애니메이션 효과
    document.body.style.animation = 'none';
    setTimeout(() => {
        document.body.style.animation = 'fadeIn 0.5s ease';
    }, 10);
}

/* ========================
   투두 리스트 기능
   ======================== */

function addTodo() {
    const input = document.getElementById('todoInput');
    const todoText = input.value.trim();

    // 빈 입력값 검증
    if (todoText === '') {
        alert('할 일을 입력해주세요!');
        return;
    }

    const todoItems = document.getElementById('todoItems');
    const newTodoItem = document.createElement('li');
    newTodoItem.className = 'todo-item';

    newTodoItem.innerHTML = `
        <span>${escapeHtml(todoText)}</span>
        <button onclick="removeTodo(this)">×</button>
    `;

    todoItems.appendChild(newTodoItem);
    input.value = '';
    input.focus();
}

function removeTodo(button) {
    const todoItem = button.parentElement;
    
    // 삭제 애니메이션
    todoItem.style.animation = 'slideUp 0.3s ease';
    
    setTimeout(() => {
        todoItem.remove();
    }, 300);
}

// 투두 입력에서 Enter 키 처리
document.addEventListener('DOMContentLoaded', function() {
    const todoInput = document.getElementById('todoInput');
    if (todoInput) {
        todoInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                addTodo();
            }
        });
    }
});

/* ========================
   텍스트 통계 분석 기능
   ======================== */

function analyzeText() {
    const textArea = document.getElementById('textArea');
    const text = textArea.value;
    const statsResult = document.getElementById('statsResult');

    if (text.trim() === '') {
        statsResult.innerHTML = '<p style="grid-column: 1/-1; text-align: center; color: #e74c3c;">📝 텍스트를 입력해주세요!</p>';
        return;
    }

    // 통계 계산
    const charCount = text.length;
    const charCountNoSpace = text.replace(/\s/g, '').length;
    const wordCount = text.trim().split(/\s+/).length;
    const lineCount = text.split('\n').length;
    const spaceCount = text.split(' ').length - 1;

    // 가장 많이 사용된 문자
    const charFrequency = {};
    for (let char of text.toLowerCase()) {
        if (char !== ' ' && char !== '\n') {
            charFrequency[char] = (charFrequency[char] || 0) + 1;
        }
    }

    let mostUsedChar = '';
    let maxCount = 0;
    for (let char in charFrequency) {
        if (charFrequency[char] > maxCount) {
            maxCount = charFrequency[char];
            mostUsedChar = char;
        }
    }

    // 평균 단어 길이
    const words = text.trim().split(/\s+/);
    const avgWordLength = (charCountNoSpace / wordCount).toFixed(2);

    // 결과 표시
    statsResult.innerHTML = `
        <div class="stat-item">
            <div class="label">📊 전체 문자</div>
            <div class="value">${charCount}</div>
        </div>
        <div class="stat-item">
            <div class="label">🔤 공백 제외</div>
            <div class="value">${charCountNoSpace}</div>
        </div>
        <div class="stat-item">
            <div class="label">📝 단어 수</div>
            <div class="value">${wordCount}</div>
        </div>
        <div class="stat-item">
            <div class="label">📄 줄 수</div>
            <div class="value">${lineCount}</div>
        </div>
        <div class="stat-item">
            <div class="label">🔤 평균 단어 길이</div>
            <div class="value">${avgWordLength}</div>
        </div>
        <div class="stat-item">
            <div class="label">✨ 자주 쓰는 문자</div>
            <div class="value">${mostUsedChar || '-'}</div>
        </div>
    `;
}

/* ========================
   XSS 방지 함수
   ======================== */

function escapeHtml(unsafe) {
    return unsafe
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}

/* ========================
   페이지 로드 완료 후 초기화
   ======================== */

document.addEventListener('DOMContentLoaded', function() {
    console.log('✅ 웹 페이지 로드 완료!');
    console.log('HTML5, CSS3, JavaScript 학습을 시작하세요!');

    // 페이지 로드 시 배경색 초기화
    document.body.style.backgroundColor = '#f5f7fa';
});

/* ========================
   스크롤 애니메이션
   ======================== */

// Intersection Observer를 사용한 스크롤 애니메이션
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver(function(entries) {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

document.addEventListener('DOMContentLoaded', function() {
    const cards = document.querySelectorAll('.card');
    const practiceBoxes = document.querySelectorAll('.practice-box');

    cards.forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        observer.observe(card);
    });

    practiceBoxes.forEach(box => {
        box.style.opacity = '0';
        box.style.transform = 'translateY(20px)';
        observer.observe(box);
    });
});

/* ========================
   키보드 단축키
   ======================== */

document.addEventListener('keydown', function(e) {
    // Ctrl + K로 계산기 입력 포커스
    if (e.ctrlKey && e.key === 'k') {
        e.preventDefault();
        const num1Input = document.getElementById('num1');
        if (num1Input) {
            num1Input.focus();
        }
    }

    // Ctrl + T로 투두 입력 포커스
    if (e.ctrlKey && e.key === 't') {
        e.preventDefault();
        const todoInput = document.getElementById('todoInput');
        if (todoInput) {
            todoInput.focus();
        }
    }
});
