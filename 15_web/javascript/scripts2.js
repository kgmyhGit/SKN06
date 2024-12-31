// script2.js

// 한줄 주석 - control + /
/*  block 주석 - 여러줄 주석에 사용.  */

//1. 함수 정의
function hello1() {
    alert("경고입니다.");
}
// hello1()
// hello1()

//2. parameter(매개변수) 가 있는 함수
function hello2(name, age) {
    alert("hello2");
    alert(`이름: ${name}, 나이: ${age}`);
    if (!name) {
        alert("이름 입력");
    }
}
// hello2("홍길동", 30)
// hello2(null, 30)
// hello2(age=30) // 30->name에 대입.


//5. 기본값이 있는 파라미터.
function hello3(name = "무명", age = 0) {
    console.log(`이름: ${name}, 나이: ${age}`);
}
// hello3("이순신", 20)
// hello3()

//4. 반환값이 있는 함수
function hello4() {
    let name = prompt("이름을 입력하세요"); //사용자 입력
    return `이름 : ${name}`;
}
// let info = hello4()
// console.log(info)


//5. Rest Parameter (파이썬-가변인자 *args)
function hello5(name, age, ...other) {
    console.log(name, age);
    console.log(other);
}
// hello5("이순신", 20, "서울", "170cm", "B형")
// hello5("이순신", 20)

//6. 함수 리터럴.
let hello6 = function(name) {
    alert(name);
};
// hello6("홍길동")

//7. 함수를 argument로 전달.
function worker(func) {
    num1 = 10;
    num2 = 20;
    result = func(num1, num2);
    console.log("계산결과: " + result);
}

function sum(n1, n2) {
    return n1 + n2;
}

// worker(sum)
// worker(function(n1, n2){return n1 - n2})
// worker((n1, n2)=>{return n1 * n2})


//8. 화살표 함수
let arrowFunc1 = (num1, num2) => num1 + num2;

// let result = arrowFunc1(10, 20)
// console.log(result)

let arrowFunc2 = (num1, num2) => {
    result = num1 - num2;
    console.log(result);
    return result
};
// result2 = arrowFunc2(100, 200);
// console.log("arrowFunc2", result2)