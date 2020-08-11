---
title: CPP补充知识点记录
subtitle: CPP补充知识点记录
date: 2019-12-07
tags: ["coding"]
bigimg: [{src: "https://images.pexels.com/photos/3455450/pexels-photo-3455450.jpeg?cs=srgb&dl=woman-in-yellow-pants-lying-on-concrete-tiled-floor-3455450.jpg&fm=jpg", desc: "https://www.pexels.com/"}]
---

一些CPP学习的记录

<!--more-->

# CPP补充知识点记录

* [CPP补充知识点记录](#cpp补充知识点记录)
  + [类&对象](#类对象)
    - [默认配置](#默认配置)
    - [静态成员](#静态成员)
      - [静态成员函数](#静态成员函数)
    - [对象数组初始化](#对象数组初始化)
    - [赋值兼容规则](#赋值兼容规则)
    - [构造函数&析构函数](#构造函数析构函数)
      - [类的构造函数](#类的构造函数)
      - [使用初始化列表来初始化字段](#使用初始化列表来初始化字段)
      - [类的析构函数](#类的析构函数)
      - [new&delete](#newdelete)
      - [拷贝构造函数](#拷贝构造函数)
    - [内联函数](#内联函数)
    - [友元函数&友元类](#友元函数友元类)
    - [类访问修饰符](#类访问修饰符)
      - [三种访问控制下继承的差异](#三种访问控制下继承的差异)
    - [this指针](#this指针)
    - [常函数](#常函数)
    - [virtual](#virtual)
      - [虚基类](#虚基类)
      - [虚函数（多态）](#虚函数多态)
      - [纯虚函数](#纯虚函数)
  + [作用域](#作用域)
  + [指针数组&数组指针](#指针数组数组指针)
    - [数组指针（也称**行指针**）](#数组指针也称行指针)
    - [指针数组](#指针数组)
    - [小结](#小结)
  + [命令行参数](#命令行参数)

## 类&对象

### 默认配置

C++为类（Class）提供了许多默认函数。如果自己没有申明，编译器会为我们提供一个 `copy构造函数` 、一个 `copy assignment操作符` 和一个 `析构函数` 。此外，如果没有申明任何 `构造函数` ，编译器会为我们申明一个 `default构造函数` 。很像下面的Empty类：

``` cpp
class Empty{
    public:
        Empty();
        Empty(const Empty &rhs);
        ~Empty();
        Empty& operator=(const Empty &rhs);
};
```

像Effective C++说的，如果不想使用编译器自动生成的函数，就应该明确拒绝。

### 静态成员

我们可以使用 `static` 关键字来把类成员定义为静态的。当我们声明类的成员为静态时，这意味着**无论创建多少个类的对象，静态成员都只有一个副本**。

静态成员在类的所有对象中是共享的。**如果不存在其他的初始化语句，在创建第一个对象时，所有的静态数据都会被初始化为零**。我们**不能把静态成员的初始化放置在类的定义中，但是可以在类的外部通过使用范围解析运算符 `::` 来重新声明静态变量从而对它进行初始化**，如下面的实例所示。

``` cpp
#include <iostream>
 
using namespace std;
 
class Box
{
   public:
      static int objectCount;
      // 构造函数定义
      Box(double l=2.0, double b=2.0, double h=2.0)
      {
         cout <<"Constructor called." << endl;
         length = l;
         breadth = b;
         height = h;
         // 每次创建对象时增加 1
         objectCount++;
      }
      double Volume()
      {
         return length * breadth * height;
      }
   private:
      double length;     // 长度
      double breadth;    // 宽度
      double height;     // 高度
};
 
// 初始化类 Box 的静态成员
int Box::objectCount = 0;
 
int main(void)
{
   Box Box1(3.3, 1.2, 1.5);    // 声明 box1
   Box Box2(8.5, 6.0, 2.0);    // 声明 box2
 
   // 输出对象的总数
   cout << "Total objects: " << Box::objectCount << endl;
 
   return 0;
}
```

当上面的代码被编译和执行时，它会产生下列结果：

``` 
Constructor called.
Constructor called.
Total objects: 2
```

#### 静态成员函数

如果把函数成员声明为静态的，就可以把函数与类的任何特定对象独立开来。**静态成员函数即使在类对象不存在的情况下也能被调用**，静态函数只要使用类名加范围解析运算符 `::` 就可以访问。（有点类似于python中的类方法）

静态成员函数只能访问**静态成员数据、其他静态成员函数和类外部的其他函数**。

静态成员函数有一个类范围，他们**不能访问类的 `this` 指针**。您**可以使用静态成员函数来判断类的某些对象是否已被创建**。

静态成员函数与普通成员函数的区别：

* 静态成员函数没有 `this` 指针，**只能访问静态成员**（包括静态成员变量和静态成员函数）。
* 普通成员函数有 `this` 指针，可以访问类中的任意成员。

下面的实例有助于更好地理解静态成员函数的概念：

``` cpp
#include <iostream>
 
using namespace std;
 
class Box
{
   public:
      static int objectCount;
      // 构造函数定义
      Box(double l=2.0, double b=2.0, double h=2.0)
      {
         cout <<"Constructor called." << endl;
         length = l;
         breadth = b;
         height = h;
         // 每次创建对象时增加 1
         objectCount++;
      }
      double Volume()
      {
         return length * breadth * height;
      }
      static int getCount()
      {
         return objectCount;
      }
   private:
      double length;     // 长度
      double breadth;    // 宽度
      double height;     // 高度
};
 
// 初始化类 Box 的静态成员
int Box::objectCount = 0;
 
int main(void)
{
  
   // 在创建对象之前输出对象的总数
   cout << "Inital Stage Count: " << Box::getCount() << endl;
 
   Box Box1(3.3, 1.2, 1.5);    // 声明 box1
   Box Box2(8.5, 6.0, 2.0);    // 声明 box2
 
   // 在创建对象之后输出对象的总数
   cout << "Final Stage Count: " << Box::getCount() << endl;
 
   return 0;
}
```

当上面的代码被编译和执行时，它会产生下列结果：

``` 
Inital Stage Count: 0
Constructor called.
Constructor called.
Final Stage Count: 2
```

### 对象数组初始化

对象数组：数组中每个元素为一个对象。在建立数组时，可以在定义数组时提供实参以实现初始化。

1. 如果**构造函数只有一个参数**，可以直接在等号后面的花括号内提供实参，如：

``` cpp
Student stu[3]={10,20,30}；
```

2. 如果**构造函数有多个参数**，在定义时在花括号中分别写出构造函数名并在括号内指定实参。在建立对象数组时，分别调用构造函数，对每个元素进行初始化。每个元素的实参分别用括号括起来，对应构造函数的一组形参，不会混淆。如下：

``` cpp
// 构造函数有3个参数，分别代表学号，年龄，成绩，在定义时可以：
Student stu【3】={
  Student(1001,18,80),
  Student(1001,18,80),
  Student(1001,18,80),
};
```

### 赋值兼容规则

不同类型的数据之间的自动转换和赋值，称为赋值兼容。在**基类和派生类对象之间也存在有赋值兼容关系**，基类和派生类对象之间的赋值兼容规则是指**在需要基类对象的任何地方，都可以使用公有派生类的对象来替代**。

根据赋值兼容规则，在基类 `Base` 的对象可以使用的任何地方，都可以用派生类 `Derived` 的对象来替代，但只能使用从基类继承来的成员。具体体现在以下几个方面：

``` cpp
class Base{
   ......
};
class Derived:public Base{
   ......
};
```

* 派生类对象可以向基类对象赋值，即用**派生类对象中从基类继承来的数据成员逐个赋值给基类对象的数据成员**。

``` cpp
Base b;			//定义基类 Base 的对象 b
Derived d;		//定义基类 Base 的公有派生类 Derived 的对象 d
b=d;			//用派生类 Derived 的对象 d 对基类对象 b 赋值
```

* 派生类对象可以初始化基类对象的引用。

``` cpp
Base b;		//定义基类 Base 的对象 b
Derived d;		//定义基类 Base 的公有派生类 Derived 的对象 d
Base &br=d;		//定义基类 Base 的对象的引用 br，并用派生类 Derived 的对象 d 对其初始化
```

* 派生类对象的地址可以赋给指向基类对象的指针。(最常见到)

``` cpp
Derived d;	//定义基类 Base 的公有派生类 Derived 的对象 d
Base *bp=&d;	//把派生类对象的地址 &d 赋值给指向基类的指针 bp，
        //即，使指向基类对象的指针 bp 也可以指向派生类对象 d
```

* 如果函数的形参是基类对象或基类对象的引用，在调用函数时可以用派生类对象作为实参。

``` cpp
class Base{
  public:
    int i;
    ··· ···
};
class Derived:public Base{		//定义基类 Base 的公有派生类 Derived
    ··· ···
};
void fun(Base &bb){		//普通函数，形参为基类 Base 对象的引用
  cout<<bb.i<<endl;		//输出该引用所代表的对象的数据成员 i
}
```

在调用函数 `fun` 时可以用派生类 `Derived` 的对象 `d4` 作为实参：

``` cpp
fun(d4)
```

输出派生类 `Derived` 的对象 `d4` 赋给基类数据成员 `i` 的值。

* 声明为基类对象的指针可以指向它的公有派生的对象，但**不允许指向它的私有派生、保护派生的对象**。

``` cpp
class Base {
public:
  void pbase() { cout << "base" << endl; }
};
class Derived : private Base { //定义私有派生类 Derived
  void pderive() { cout << "derive" << endl; }
};
int main() {
  Base op1, *ptr; //定义基类 Base 的对象 op1 及指向基类 Base 的指针 ptr
  Derived op2; //定义派生类 Derived 的对象 op2
  ptr = &op1;  //将指针 ptr 指向基类对象 op1
  ptr = &op2; //错误，不允许将指向基类 Base 的指针 ptr 指向它的私有派生类对象op2

  return 0;
}

class Base {
public:
  void pbase() { cout << "base" << endl; }
};
class Derived : protected Base { //定义保护派生类 Derived
  void pderive() { cout << "derive" << endl; }
};
int main() {
  Base op1, *ptr; //定义基类 Base 的对象 op1 及指向基类 Base 的指针 ptr
  Derived op2; //定义派生类 Derived 的对象 op2
  ptr = &op1;  //将指针 ptr 指向基类对象 op1
  ptr = &op2; //允许将指向基类 Base 的指针 ptr 指向它的非私有派生类对象op2

  return 0;
}
```

* **不能将一个声明为指向派生类对象的指针指向其基类对象**。

``` cpp
class Base {
public:
  void pbase() { cout << "base" << endl; }
};
class Derived : public Base { //定义公有派生类 Derived
  void pderive() { cout << "derive" << endl; }
};
int main() {
  Base obj1;          //定义基类对象 obj1
  Derived obj2, *ptr; //定义派生类对象 obj2 及指向派生类的指针 ptr
  ptr = &obj2; //将指向派生类对象的指针 ptr 指向派生类对象 obj2
  ptr = &obj1; //错误，将指向派生类对象的指针 ptr 指向其基类对象 obj1

  return 0;
}
```

* 声明为指向基类对象的指针**不可以直接访问该基类派生类新定义的成员**。（这看上去和虚函数的设定有些类似，没有声明 `virtual` 的时候，基类指针会自动调用基类的成员）

``` cpp
class Base {
public:
  void pbase() { cout << "base" << endl; }
};
class Derived : public Base { //定义私有派生类 Derived
  void pderive() { cout << "derive" << endl; }
};
int main() {
  Base op1, *ptr; //定义基类 Base 的对象 op1 及指向基类 Base 的指针 ptr
  Derived op2; //定义派生类 Derived 的对象 op2
  ptr = &op1;  //将指针 ptr 指向基类对象 op1
  ptr->pbase();`
  ptr = &op2; //错误，不允许将指向基类 Base 的指针 ptr 指向它的私有派生类对象op2
  ptr->pbase();
  ptr->pderive(); // No member named 'pderive' in 'Base'

  return 0;
}
```

> 参考自：https://blog.csdn.net/aaqian1/article/details/84979261

### 构造函数&析构函数

#### 类的构造函数

类的一种特殊的成员函数，它会在每次创建类的新对象时执行。构造函数的名称与类的名称是完全相同的，并且不会返回任何类型，也不会返回 void。构造函数可用于为某些成员变量设置初始值。

``` cpp
#include <iostream>
 
using namespace std;
 
class Line
{
   public:
      void setLength( double len );
      double getLength( void );
      Line();  // 这是构造函数
 
   private:
      double length;
};
 
// 成员函数定义，包括构造函数
Line::Line(void)
{
    cout << "Object is being created" << endl;
}
 
void Line::setLength( double len )
{
    length = len;
}
 
double Line::getLength( void )
{
    return length;
}
// 程序的主函数
int main( )
{
   Line line;
 
   // 设置长度
   line.setLength(6.0); 
   cout << "Length of line : " << line.getLength() <<endl;
 
   return 0;
}

输出：
Object is being created
Length of line : 6
```

默认的构造函数没有任何参数，但如果需要，构造函数也可以带有参数。这样在创建对象时就会给对象赋初始值。

``` cpp
#include <iostream>
 
using namespace std;
 
class Line
{
   public:
      void setLength( double len );
      double getLength( void );
      Line(double len);  // 这是构造函数
 
   private:
      double length;
};
 
// 成员函数定义，包括构造函数
Line::Line( double len)
{
    cout << "Object is being created, length = " << len << endl;
    length = len;
}
 
void Line::setLength( double len )
{
    length = len;
}
 
double Line::getLength( void )
{
    return length;
}
// 程序的主函数
int main( )
{
   Line line(10.0);
 
   // 获取默认设置的长度
   cout << "Length of line : " << line.getLength() <<endl;
   // 再次设置长度
   line.setLength(6.0); 
   cout << "Length of line : " << line.getLength() <<endl;
 
   return 0;
}

输出：
Object is being created, length = 10
Length of line : 10
Length of line : 6
```

#### 使用初始化列表来初始化字段

使用初始化列表来初始化字段：

``` cpp
Line::Line( double len): length(len)
{
    cout << "Object is being created, length = " << len << endl;
}
```

上面的语法等同于如下语法：

``` cpp
Line::Line( double len)
{
    length = len;
    cout << "Object is being created, length = " << len << endl;
}
```

假设有一个类 C，具有多个字段 X、Y、Z 等需要进行初始化，同理地，您可以使用上面的语法，只需要在不同的字段使用逗号进行分隔，如下所示：

``` cpp
C::C( double a, double b, double c): X(a), Y(b), Z(c)
{
  ....
}
```

初始化列表的成员初始化顺序：C++ **初始化类成员时，是按照声明的顺序初始化的，而不是按照出现在初始化列表中的顺序**。

``` cpp
class CMyClass {
    CMyClass(int x, int y);
    int m_x;
    int m_y;
};

CMyClass::CMyClass(int x, int y) : m_y(y), m_x(m_y)
{
    ...
};
```

你可能以为上面的代码将会首先做 `m_y=y` ，然后做 `m_x=m_y` ，最后它们有相同的值。

但是编译器实际上**先初始化 `m_x` ，然后是 `m_y` **，因为它们**是按这样的顺序声明**的。结果是 `m_x` 将有一个不可预测的值。

有两种方法避免它：

1. 一个是**总是按照你希望它们被初始化的顺序声明成员**
2. 第二个是，如果你决定使用初始化列表，**总是按照它们声明的顺序罗列这些成员**，这将有助于消除混淆

#### 类的析构函数

类的一种特殊的成员函数，它会在每次删除所创建的对象时执行。

析构函数的名称与类的名称是完全相同的，只是在前面加了个波浪号（~）作为前缀，它不会返回任何值，也不能带有任何参数。**析构函数有助于在跳出程序（比如关闭文件、释放内存等）前释放资源**。

谨慎对待析构函数, 析构函数往往比其表面看起来要更长, 因为有隐含的成员和基类析构函数被调用!

``` cpp
#include <iostream>
 
using namespace std;
 
class Line
{
   public:
      void setLength( double len );
      double getLength( void );
      Line();   // 这是构造函数声明
      ~Line();  // 这是析构函数声明
 
   private:
      double length;
};
 
// 成员函数定义，包括构造函数
Line::Line(void)
{
    cout << "Object is being created" << endl;
}
Line::~Line(void)
{
    cout << "Object is being deleted" << endl;
}
 
void Line::setLength( double len )
{
    length = len;
}
 
double Line::getLength( void )
{
    return length;
}
// 程序的主函数
int main( )
{
   Line line;
 
   // 设置长度
   line.setLength(6.0); 
   cout << "Length of line : " << line.getLength() <<endl;
 
   return 0;
}

当上面的代码被编译和执行时，它会产生下列结果：
Object is being created
Length of line : 6
Object is being deleted
```

#### new&delete

1. 当你使用 `new` 时，有两件事会发生，第一，内存被配置（透过函数 `operator new` ）。第二，会有一个（或以上）的 `constructors` 针对此内存被调用。当你使用 `delete` 时，也有两件事发生：一个（或以上）的 `destructors` 会针对此内存被调用，然后内存被释放（透过函数 `operator delete` ）。
2. 如果你使用 `delete` 未加方括号， `delete` 便**假设删除对象是单一对象**。否则便假设删除对象是个数组。

``` cpp
string *stringPtr1 = new string;
string *stringPtr2 = new string[100];
…
delete stringPtr1;
delete [] stringPtr2;
```

如果你对 `stringPtr1` 使用了 `[]` 形式会发生什么呢？结果是未定义的，但不太可能是什么好事。假设如上图的布局， `delete` 将读入某些内存的内容并将其看作一个数组的大小，然后开始调用那么多析构函数，不仅全然不顾它在其上工作的内存不是数组，而且还可能忘掉了它正忙着析构的对象的类型。如果你对 `stringPtr2` 没有使用 `[]` 形式会发生什么呢？也是未定义的，只不过你不会看到它会引起过多的析构函数被调用。此外，**对于类似 `int` 的内建类型其结果也是未定义的**（而且有时是有害的），即使这样的类型没有析构函数。

3. 因此，游戏规则很简单，如果你在调用 `new` 时使用了 `[]` ，则你在调用delete时也使用 `[]` ，如果你在调用 `new` 的时候没有 `[]` ，那么你也不应该在调用时使用 `[]` 。

#### 拷贝构造函数

拷贝构造函数是一种特殊的构造函数，它在创建对象时，是使用**同一类中之前创建的对象来初始化新创建的对象**。拷贝构造函数通常用于：

1. 通过使用另一个同类的对象来初始化新创建的对象。
2. 复制对象把它作为参数传递给函数。
3. 复制对象，并从函数返回这个对象。

必须定义拷贝构造函数的情况：只包含类类型成员或内置类型（但不是指针类型）成员的类，无须显式地定义拷贝构造函数也可以拷贝；有的类有一个数据成员是指针，或者是有成员表示在构造函数中分配的其他资源，这两种情况下都必须定义拷贝构造函数。

* **如果在类中没有定义拷贝构造函数，编译器会自行定义一个**。
* 如果类带有指针变量，并有动态内存分配，则它必须有一个拷贝构造函数。

拷贝构造函数的最常见形式如下：

``` cpp
classname (const classname &obj) {
   // 构造函数的主体
}
```

在这里， `obj` 是一个对象引用，该对象是用于初始化另一个对象的。

``` cpp
#include <iostream>

using namespace std;

class Line {
public:
  int getLength(void);
  Line(int len);         // 简单的构造函数
  Line(const Line &obj); // 拷贝构造函数
  ~Line();               // 析构函数

private:
  int *ptr;
};

// 成员函数定义，包括构造函数
Line::Line(int len) {
  cout << "调用构造函数" << endl;
  // 为指针分配内存
  ptr = new int;
  *ptr = len;
}

Line::Line(const Line &obj) {
  cout << "调用拷贝构造函数并为指针 ptr 分配内存" << endl;
  ptr = new int;
  *ptr = *obj.ptr; // 拷贝值
}

Line::~Line(void) {
  cout << "释放内存" << endl;
  delete ptr;
}

int Line::getLength(void) { return *ptr; }

void display(Line obj) { cout << "line 大小 : " << obj.getLength() << endl; }

// 程序的主函数
int main() {
  Line line(10);
  display(line);  // 在传入display的时候，对临时变量obj进行了拷贝构造，所以有对应输出

  return 0;
}
```

当上面的代码被编译和执行时，它会产生下列结果：

``` 
调用构造函数
调用拷贝构造函数并为指针 ptr 分配内存
line 大小 : 10
释放内存
释放内存
```

下面的实例对上面的实例稍作修改，通过使用已有的同类型的对象来初始化新创建的对象：

``` cpp
#include <iostream>

using namespace std;

class Line {
public:
  int getLength(void);
  Line(int len);         // 简单的构造函数
  Line(const Line &obj); // 拷贝构造函数
  ~Line();               // 析构函数

private:
  int *ptr;
};

// 成员函数定义，包括构造函数
Line::Line(int len) {
  cout << "调用构造函数" << endl;
  // 为指针分配内存
  ptr = new int;
  *ptr = len;
}

Line::Line(const Line &obj) {
  cout << "调用拷贝构造函数并为指针 ptr 分配内存" << endl;
  ptr = new int;
  *ptr = *obj.ptr; // 拷贝值
}

Line::~Line(void) {
  cout << "释放内存" << endl;
  delete ptr;
}

int Line::getLength(void) { return *ptr; }

void display(Line obj) { cout << "line 大小 : " << obj.getLength() << endl; }

// 程序的主函数
int main() {
  Line line1(10);
  Line line2 = line1; // 这里也调用了拷贝构造函数

  display(line1); // 在传入display的时候，对临时变量obj进行了拷贝构造，所以有对应输出
  display(line2);

  return 0;
}
```

当上面的代码被编译和执行时，它会产生下列结果：

``` 
调用构造函数
调用拷贝构造函数并为指针 ptr 分配内存
调用拷贝构造函数并为指针 ptr 分配内存
line 大小 : 10
释放内存
调用拷贝构造函数并为指针 ptr 分配内存
line 大小 : 10
释放内存
释放内存
释放内存
```

C++支持两种初始化形式：

1. 拷贝初始化 `int a = 5` 
2. 直接初始化 `int a(5)` 

对于其他类型没有什么区别，对于类类型直接初始化直接调用实参匹配的构造函数，拷贝初始化总是调用拷贝构造函数，也就是说：

``` cpp
A x(2);　　//直接初始化，调用构造函数
A y = x;　　//拷贝初始化，调用拷贝构造函数
```

**注意：**根据文章<https://blog.csdn.net/ljianhui/article/details/9245661#>的分析，由于编译器的优化，会导致直接初始化和拷贝初始化最终调用构造函数的选择情况略有不同。

``` cpp
#include <cstring>
#include <iostream>
using namespace std;

class ClassTest {
public:
  ClassTest() {
    c[0] = '\0';
    cout << "ClassTest()" << endl;
  }

  ClassTest &operator=(const ClassTest &ct) {
    strcpy(c, ct.c);
    cout << "ClassTest& operator=(const ClassTest &ct)" << endl;
    return *this;
  }

  ClassTest(const char *pc) {
    strcpy(c, pc);
    cout << "ClassTest (const char *pc)" << endl;
  }

  // private:
  ClassTest(const ClassTest &ct) {
    strcpy(c, ct.c);
    cout << "ClassTest(const ClassTest& ct)" << endl;
  }

private:
  char c[256]{};
};

int main() {
  cout << "ct1: ";
  ClassTest ct1("ab"); //直接初始化
  cout << "ct2: ";
  ClassTest ct2 = "ab"; //复制初始化
  cout << "ct2 =: ";
  ct2 = "ab"; //这里依然涉及到复制拷贝到临时变量的过程，所以会有两部分输出
  cout << "ct3: ";
  ClassTest ct3 = ct1; //复制初始化
  cout << "ct4: ";
  ClassTest ct4(ct1); //直接初始化
  cout << "ct5: ";
  ClassTest ct5 = ClassTest(); //复制初始化
  return 0;
}
```

虽然初始化方式不同，但是编译器优化后，输出出乎我们所料，而且这里的复制操作符也没有被使用：

``` 
ct1: ClassTest (const char *pc)
ct2: ClassTest (const char *pc)
ct2 =: ClassTest (const char *pc)
ClassTest& operator=(const ClassTest &ct)
ct3: ClassTest(const ClassTest& ct)
ct4: ClassTest(const ClassTest& ct)
ct5: ClassTest()
```

### 内联函数

定义: 当函数被声明为内联函数之后, 编译器会将其内联展开, 而不是按通常的函数调用机制进行调用。内联函数是通常与类一起使用。如果一个函数是内联的，那么**在编译时，编译器会把该函数的代码副本放置在每个调用该函数的地方**。

对内联函数进行任何修改，都需要重新编译函数的所有客户端，因为编译器需要重新更换一次所有的代码，否则将会继续使用旧的函数。

如果想把一个函数定义为内联函数，则需要在函数名前面放置关键字 `inline` ，在调用函数之前需要对函数进行定义。**如果已定义的函数多于一行，编译器会忽略 `inline` 限定符。在类内定义中的定义的函数都是内联函数，即使没有使用 `inline` 说明符。**

**引入内联函数的目的**：为了解决程序中函数调用的效率问题。程序在编译器编译的时候，编译器将程序中出现的内联函数的调用表达式用内联函数的函数体进行替换，而**对于其他的函数，都是在运行时候才被替代**。这其实就是个**空间代价换时间的节省**。

* 优点: 当函数体比较小的时候, 内联该函数可以令目标代码更加高效. 对于存取函数以及其它函数体比较短, 性能关键的函数, 鼓励使用内联。
* 缺点: 滥用内联将导致程序变慢. 内联可能使目标代码量或增或减, 这取决于内联函数的大小. 内联非常短小的存取函数通常会减少代码大小, 但内联一个相当大的函数将戏剧性的增加代码大小. 现代处理器由于更好的利用了指令缓存, 小巧的代码往往执行更快。
* 结论: 一个较为合理的经验准则是, **不要内联超过 10 行的函数**。只有当函数只有 10 行甚至更少时才将其定义为内联函数。

在使用内联函数时要留神：

1. 在内联函数内**不允许使用循环语句和开关语句**， 内联那些包含循环或 switch 语句的函数常常是得不偿失（除非在大多数情况下, 这些循环或 switch 语句从不被执行）；
2. 内联函数的**定义必须出现在内联函数第一次调用之前**；
3. **在所在的类内部定义的函数是内联函数**。
4. **有些函数即使声明为内联的也不一定会被编译器内联**, 这点很重要; 比如**虚函数和递归函数就不会被正常内联**。

   1. 通常, 递归函数不应该声明成内联函数。（递归调用堆栈的展开并不像循环那么简单, 比如递归层数在编译时可能是未知的, 大多数编译器都不支持内联递归函数）
   2. 虚函数内联的主要原因则是想把它的函数体放在类定义内, 为了图个方便, 抑或是当作文档描述其行为, 比如精短的存取函数.

下面是一个实例，使用内联函数来返回两个数中的最大值：（要注意这里虽然没有使用类，但是内联函数依旧可以使用）

``` cpp
#include <iostream>
 
using namespace std;

inline int Max(int x, int y)
{
   return (x > y)? x : y;
}

// 程序的主函数
int main( )
{
   cout << "Max (20,10): " << Max(20,10) << endl;
   cout << "Max (0,200): " << Max(0,200) << endl;
   cout << "Max (100,1010): " << Max(100,1010) << endl;
   return 0;
}
```

当上面的代码被编译和执行时，它会产生下列结果：

``` 
Max (20,10): 20
Max (0,200): 200
Max (100,1010): 1010
```

### 友元函数&友元类

类的友元函数是定义在类外部，但有权访问类的所有私有（private）成员和保护（protected）成员。尽管友元函数的原型有在类的定义中出现过，但是**友元函数并不是成员函数**。

友元可以是一个函数，该函数被称为**友元函数**；友元也可以是一个类，该类被称为**友元类**，在这种情况下，*整个类及其所有成员都是友元*。

如果要声明函数为一个类的友元，需要在类定义中该函数原型前使用关键字 `friend` ，如下所示：

``` cpp
class Box
{
   double width;
public:
   double length;
   friend void printWidth( Box box );
   void setWidth( double wid );
};
```

声明类 `ClassTwo` 的所有成员函数作为类 `ClassOne` 的友元，需要在类 `ClassOne` 的定义中放置如下声明：

``` cpp
friend class ClassTwo;
```

请看下面的程序：

``` cpp
#include <iostream>
 
using namespace std;
 
class Box
{
   double width;
public:
   friend void printWidth( Box box );
   void setWidth( double wid );
};
 
// 成员函数定义
void Box::setWidth( double wid )
{
    width = wid;
}
 
// 请注意：printWidth() 不是任何类的成员函数
void printWidth( Box box )
{
   /* 因为 printWidth() 是 Box 的友元，它可以直接访问该类的任何成员 */
   cout << "Width of box : " << box.width <<endl;
}
 
// 程序的主函数
int main( )
{
   Box box;
 
   // 使用成员函数设置宽度
   box.setWidth(10.0);
   
   // 使用友元函数输出宽度
   printWidth( box );
 
   return 0;
}
```

当上面的代码被编译和执行时，它会产生下列结果：

``` 
Width of box : 10
```

### 类访问修饰符

数据封装是面向对象编程的一个重要特点，它防止函数直接访问类类型的内部成员。类成员的访问限制是通过在类主体内部对各个区域标记 `public` 、 `private` 、 `protected` 来指定的。关键字 `public` 、 `private` 、 `protected` 称为访问修饰符。

一个类可以有多个 `public` 、 `protected` 或 `private` 标记区域。每个标记区域在下一个标记区域开始之前或者在遇到类主体结束右括号之前都是有效的。

成员和类的**默认访问修饰符是 `private` **。

1. 公有成员在程序中类的外部是可访问的。您可以不使用任何成员函数来设置和获取公有变量的值。
2. 私有成员变量或函数在类的外部是不可访问的，甚至是不可查看的。只有类和友元函数可以访问私有成员。**默认情况下，类的所有成员都是私有的。**
3. 保护成员变量或函数与私有成员十分相似，但有一点不同，保护成员在派生类（即子类）中是可访问的。

#### 三种访问控制下继承的差异

有 `public` , `protected` , `private` 三种继承方式，它们相应地改变了基类成员的访问属性。要注意，默认是私有派生。

1. `public` 继承：子类继承基类的 `public` 成员， `protected` 成员，对应的访问属性在派生类中分别变成： `public` , `protected` ，但是 `private` 成员不可访问。
2. `protected` 继承：子类继承基类的 `public` 成员， `protected` 成员，对应的访问属性在派生类中分别变成： `protected` , `protected` ，但是 `private` 成员在派生类中不可访问。
3. `private` 继承：子类继承基类的 `public` 成员， `protected` 成员，对应的访问属性在派生类中分别变成： `private` , `private` , 但是 `private` 成员在派生类中不可访问。

但要注意，通过公有继承，派生类保留了基类中**除构造函数、析构函数之外的所有成员**，基类的公有或保护成员的访问权限在派生类中全部原样保留了下来，在派生类外可以**调用基类的公有成员函数访问基类的私有成员**。因此，公有派生类具有基类的全部功能，基类能够实现的功能，公有派生类都能实现。

例子：

* `public` 继承：

``` cpp
#include<iostream>
#include<assert.h>
using namespace std;

class A{
public:
  int a;
  A(){
    a1 = 1;
    a2 = 2;
    a3 = 3;
    a = 4;
  }
  void fun(){
    cout << a << endl;    //正确
    cout << a1 << endl;   //正确
    cout << a2 << endl;   //正确
    cout << a3 << endl;   //正确
  }
public:
  int a1;
protected:
  int a2;
private:
  int a3;
};
class B : public A{
public:
  int a;
  B(int i){
    A();
    a = i;
  }
  void fun(){
    cout << a << endl;       //正确，public成员
    cout << a1 << endl;       //正确，基类的public成员，在派生类中仍是public成员。
    cout << a2 << endl;       //正确，基类的protected成员，在派生类中仍是protected可以被派生类访问。
    cout << a3 << endl;       //错误，基类的private成员不能被派生类访问。
  }
};
int main(){
  B b(10);
  cout << b.a << endl;
  cout << b.a1 << endl;   //正确
  cout << b.a2 << endl;   //错误，类外不能访问protected成员
  cout << b.a3 << endl;   //错误，类外不能访问private成员
  system("pause");
  return 0;
}
```

* `protected` 继承

    

``` cpp
#include<iostream>
#include<assert.h>
using namespace std;
class A{
public:
  int a;
  A(){
    a1 = 1;
    a2 = 2;
    a3 = 3;
    a = 4;
  }
  void fun(){
    cout << a << endl;    //正确
    cout << a1 << endl;   //正确
    cout << a2 << endl;   //正确
    cout << a3 << endl;   //正确
  }
public:
  int a1;
protected:
  int a2;
private:
  int a3;
};
class B : protected A{
public:
  int a;
  B(int i){
    A();
    a = i;
  }
  void fun(){
    cout << a << endl;       //正确，public成员。
    cout << a1 << endl;       //正确，基类的public成员，在派生类中变成了protected，可以被派生类访问。
    cout << a2 << endl;       //正确，基类的protected成员，在派生类中还是protected，可以被派生类访问。
    cout << a3 << endl;       //错误，基类的private成员不能被派生类访问。
  }
};
int main(){
  B b(10);
  cout << b.a << endl;       //正确。public成员
  cout << b.a1 << endl;      //错误，protected成员不能在类外访问。
  cout << b.a2 << endl;      //错误，protected成员不能在类外访问。
  cout << b.a3 << endl;      //错误，private成员不能在类外访问。
  system("pause");
  return 0;
}
```

* `private` 继承

``` cpp
#include<iostream>
#include<assert.h>
using namespace std;
class A{
public:
  int a;
  A(){
    a1 = 1;
    a2 = 2;
    a3 = 3;
    a = 4;
  }
  void fun(){
    cout << a << endl;    //正确
    cout << a1 << endl;   //正确
    cout << a2 << endl;   //正确
    cout << a3 << endl;   //正确
  }
public:
  int a1;
protected:
  int a2;
private:
  int a3;
};
class B : private A{
public:
  int a;
  B(int i){
    A();
    a = i;
  }
  void fun(){
    cout << a << endl;       //正确，public成员。
    cout << a1 << endl;       //正确，基类public成员,在派生类中变成了private,可以被派生类访问。
    cout << a2 << endl;       //正确，基类的protected成员，在派生类中变成了private,可以被派生类访问。
    cout << a3 << endl;       //错误，基类的private成员不能被派生类访问。
  }
};
int main(){
  B b(10);
  cout << b.a << endl;       //正确。public成员
  cout << b.a1 << endl;      //错误，private成员不能在类外访问。
  cout << b.a2 << endl;      //错误, private成员不能在类外访问。
  cout << b.a3 << endl;      //错误，private成员不能在类外访问。
  system("pause");
  return 0;
}
```

但无论哪种继承方式，上面两点都没有改变：

1. `private` 成员只能被本类成员（类内）和友元访问，不能被派生类访问；
2. `protected` 成员可以被派生类访问。

### this指针

在 C++ 中，每一个对象都能通过 `this` 指针来访问自己的地址。 `this` 指针是所有成员函数的隐含参数。因此，在成员函数内部，它可以用来指向调用对象。

友元函数没有 `this` 指针，因为友元不是类的成员。只有成员函数才有 `this` 指针。

``` cpp
#include <iostream>
 
using namespace std;
 
class Box
{
   public:
      // 构造函数定义
      Box(double l=2.0, double b=2.0, double h=2.0)
      {
         cout <<"Constructor called." << endl;
         length = l;
         breadth = b;
         height = h;
      }
      double Volume()
      {
         return length * breadth * height;
      }
      int compare(Box box)
      {
         return this->Volume() > box.Volume();
      }
   private:
      double length;     // Length of a box
      double breadth;    // Breadth of a box
      double height;     // Height of a box
};
 
int main(void)
{
   Box Box1(3.3, 1.2, 1.5);    // Declare box1
   Box Box2(8.5, 6.0, 2.0);    // Declare box2
 
   if(Box1.compare(Box2))
   {
      cout << "Box2 is smaller than Box1" <<endl;
   }
   else
   {
      cout << "Box2 is equal to or larger than Box1" <<endl;
   }
   return 0;
}
```

当上面的代码被编译和执行时，它会产生下列结果：

``` 
Constructor called.
Constructor called.
Box2 is equal to or larger than Box1
```

现在来看一看以下成员函数，它是 `this` 指针的常见用法示例：

``` cpp
void Example::setValue(int a)
{
    x = a;
}
```

可以看到，该函数很自然地命名了一个形参 `a` ，用来设置成员 `x` 的值。其实这个形参 `a` 可以改成一个更加直白的标识符，使它和成员 `x` 的意思连接更明显，例如，可以使用 `xValue` 之类的，甚至可以使用 `x` 本身。

但是，一个成员函数的形参如果与类的成员具有相同的标识符，则会导致类成员被隐藏，使得它在函数内部不可访问。因此，可以使用 `this` 指针来限定类成员的名字，以使其再次可见。以下就是按这种方式重写的 setValue 成员函数：

``` cpp
void Example::setValue(int x)
{
    this->x = x;
}
```

前面讲过， `this->x` 等价于 `(*this).x` 。

### 常函数

举例： `返回类型 <类标识符::>函数名称(参数表) const` ： `bool functionName() const;` 

解释：声明了一个名为functionName的函数，该函数的返回值是bool类型。是一个常函数。

常函数作为类的成员函数，**常函数不能修改任何本类的数据成员，除非本类数据成员有 `mutable` 关键字修饰**。

说明：

1. `const` 是函数声明的一部分，在函数的实现部分也需要加上 `const` 
2. `const` 关键字**可以重载函数名相同但是未加 `const` 关键字的函数**

3.**常成员函数不能用来更新类的任何成员变量，也不能调用类中未用 `const` 修饰的成员函数，只能调用常成员函数**。即常成员函数不能更改类中的成员状态，这与 `const` 语义相符。

4. 常函数**能修改自身传入的形参**
5. 常函数的 `this` 指针是 `const classname*` （因为常函数的 `this` 指针是 `const` ，所以不能用来更新所在类的任何成员）

> 参考：https://blog.csdn.net/weixin_42744670/article/details/83380428

### virtual

#### 虚基类

``` cpp
class A
{
public:
    int iValue;
};

class B:virtual public A
{
public:
    void bPrintf(){cout<<"This is class B"<<endl;};
};

class C:virtual public A
{
public:
    void cPrintf(){cout<<"This is class C"<<endl;};
};

class D:public B,public C
{
public:
    void dPrintf(){cout<<"This is class D"<<endl;};
};

void main()
{
    D d;
    cout<<d.iValue<<endl; //正确
}
```

从代码中可以看出类 `B&C` 都继承了类 `A` 的 `iValue` 成员, 因此类 `B&C` 都有一个成员变量 `iValue` ，而类 `D` 又继承了 `B&C` ，这样类 `D` 就有一个重名的成员 `iValue` （一个是从类 `B` 中继承过来的，一个是从类 `C` 中继承过来的）。在主函数中调用 `d.iValue` 因为类 `D` 有一个重名的成员 `iValue` 编译器不知道调用从谁继承过来的 `iValue` 所以**就产生的二义性的问题**。正确的做法应该是**加上作用域限定符** `d.B::iValue` 表示调用从 `B` 类继承过来的 `iValue` 。不过类 `D` 的实例中就有多个 `iValue` 的实例，就会占用内存空间。所以C++中就引用了虚基类的概念，来解决这个问题。

在继承的类的前面加上 `virtual` 关键字**表示被继承的类是一个虚基类**，它的被继承成员**在派生类中只保留一个实例**。例如 `iValue` 这个成员，从类 `D` 这个角度上来看，它是从类 `B` 与类 `C` 继承过来的，而类 `B&C` 又是从类 `A` 继承过来的，但它们只保留一个副本。因此在主函数中调用 `d.iValue` 时就不会产生错误。

#### 虚函数（多态）

虚函数充分体现了面向对象程序设计的动态多态性。

多态按字面的意思就是多种形态。当类之间存在层次结构，并且类之间是通过继承关联时，就会用到多态。C++ **多态意味着调用成员函数时，会根据调用函数的对象的类型来执行不同的函数**。

``` cpp
#include <iostream>
using namespace std;

class Shape {
protected:
  int width, height;

public:
  Shape(int a = 0, int b = 0) {
    width = a;
    height = b;
  }
  int area() {
    cout << "Parent class area :" << endl;
    return 0;
  }
};

class Rectangle : public Shape {
public:
  Rectangle(int a = 0, int b = 0) : Shape(a, b) {}
  int area() {
    cout << "Rectangle class area :" << endl;
    return (width * height);
  }
};

class Triangle : public Shape {
public:
  Triangle(int a = 0, int b = 0) : Shape(a, b) {}
  int area() {
    cout << "Triangle class area :" << endl;
    return (width * height / 2);
  }
};

// 程序的主函数
int main() {
  Shape *shape;
  Rectangle rec(10, 7);
  Triangle tri(10, 5);

  // 存储矩形的地址
  shape = &rec;
  // 调用矩形的求面积函数 area
  shape->area();

  // 存储三角形的地址
  shape = &tri;
  // 调用三角形的求面积函数 area
  shape->area();

  return 0;
}
```

输出：

``` 
Parent class area :
Parent class area :
```

导致错误输出的原因是，调用函数 `area()` 被编译器**设置为基类中的版本，这就是所谓的静态多态，或静态链接**——函数调用在程序执行前就准备好了。有时候这也被称为**早绑定**，因为 `area()` 函数在程序编译期间就已经设置好了。

但现在，让我们对程序稍作修改，在 `Shape` 类中， `area()` 的声明前放置关键字 `virtual` ，如下所示：

``` cpp
class Shape {
protected:
  int width, height;

public:
  Shape(int a = 0, int b = 0) {
    width = a;
    height = b;
  }
  virtual int area() {
    cout << "Parent class area :" << endl;
    return 0;
  }
};
```

修改后，当编译和执行前面的实例代码时，它会产生以下结果：

``` 
Rectangle class area
Triangle class area
```

此时，**编译器看的是指针的内容，而不是它自身的类型**。因此，由于 `tri` 和 `rec` 类的对象的地址存储在 `*shape` 中，所以会调用各自的 `area()` 函数。

正如您所看到的，每个子类都有一个函数 `area()` 的独立实现。这就是多态的一般使用方式。有了多态，您可以有多个不同的类，都带有同一个名称但具有不同实现的函数，函数的参数甚至可以是相同的。

虚函数是在基类中使用关键字 `virtual` 声明的函数。在派生类中重新定义基类中定义的虚函数时，会**告诉编译器不要静态链接到该函数**。我们想要的是在程序中任意点可以根据所调用的对象类型来选择调用的函数，这种操作被称为**动态链接，或后期绑定**。

#### 纯虚函数 

您可能想要在基类中定义虚函数，以便在派生类中重新定义该函数更好地适用于对象，但是您**在基类中又不能对虚函数给出有意义的实现**，这个时候就会用到纯虚函数。

我们可以把基类中的虚函数 `area()` 改写如下：

``` cpp
class Shape {
protected:
  int width, height;

public:
  Shape(int a = 0, int b = 0) {
    width = a;
    height = b;
  }
  // pure virtual function
  virtual int area() = 0;
};
```

`= 0` 告诉编译器，函数没有主体，上面的虚函数是纯虚函数。

纯虚函数用来规范派生类的行为，即**接口**。**包含纯虚函数的类是抽象类，抽象类不能定义实例，但可以声明指向实现该抽象类的具体类的指针或引用**。

## 作用域

c++作用域可分为5类：函数原型作用域、块作用域、类作用域、文件作用域和全局（程序）作用域（跨文件）。

1. 函数原型作用域（最小的作用域）：函数原型 `int func(int x);` 这是一个函数声明，函数形参 `x` 的作用域就时所谓的函数原型作用域。
2. 块作用域：一对大括号 `{...}` 内的一段程序，块中声明的标识符作用域就是块作用域。
3. 类作用域：类成员的作用域。
4. 文件作用域（ `static` ）：全局静态变量具有全局作用域，从声明处开始，到文件（ `.cpp` 文件）结尾处结束。
5. 全局（程序）作用域（ `extern` ）：全局变量具有全局作用域，只要在使用前对其进行声明（可定义性声明/引用性声明），便可在程序（有若干个文件组成）的任意位置使用全局变量。

``` cpp
// A.h
#ifndef _A_H
#define _A_H
 
#endif

// A.cpp
#include "A.h"
int a = 5;

// B.h
#ifndef _B_H
#define _B_H
void Bfun(void);
#endif

// B.cpp
#include "B.h"
#include "A.h"
#include <IOSTREAM>
using namespace std;
extern int a; // 使用全局变量
void Bfun(void)
{
	a++;
	cout<<"Bfun: a="<<a<<",addr="<<&a<<endl;
}

// main.cpp
#include <IOSTREAM>
#include "A.h"
#include "B.h"
using namespace std;
extern int a; // 使用全局变量
int main(void)
{
	Bfun();
	cout<<"main: a="<<a<<",addr="<<&a<<endl;
	return 0;
}
```

> 例子来源：https://blog.csdn.net/u010317005/article/details/50850097

## 指针数组&数组指针

### 数组指针（也称**行指针**）

定义： `int (*p)[n];` 

`()` 优先级高，首先说明 `p` **是一个指针，指向一个整型的一维数组**，这个一维数组的长度是 `n` ，也可以说是 `p` 的步长。也就是说**执行 `p+1` 时， `p` 要跨过 `n` 个整型数据的长度**。

如要将二维数组赋给一指针，应这样赋值：

``` cpp
int a[3][4];
int (*p)[4]; //该语句是定义一个数组指针，指向含4个元素的一维数组。
p=a;         //将该二维数组的首地址赋给p，也就是 `a[0]` 或 `&a[0][0]` 
p++;         //该语句执行过后，也就是 `p=p+1;` ， `p` 跨过行 `a[0][]` 指向了行 `a[1][]` 
```

所以数组指针也称指向一维数组的指针，亦称行指针。

### 指针数组

定义： `int *p[n];` 

`[]` 优先级高，先与 `p` 结合成为一个数组，再由 `int*` 说明这是一个整型指针数组，它**有 `n` 个指针类型的数组元素**。

这里执行 `p+1` 是错误的，这样赋值也是错误的： `p=a;` ，因为 `p` 是个不可知的表示，只存在 `p[0]` 、 `p[1]` 、 `p[2]` 、... 、 `p[n-1]` ，而且它们分别是指针变量可以用来存放变量地址。但可以这样 `*p=a;` 这里 `*p` 表示指针数组第一个元素的值， `a` 的首地址的值。

如要将二维数组赋给一指针数组:

``` cpp
int *p[3];
int a[3][4];
for(i=0;i<3;i++)
  p[i]=a[i];
```

这里 `int *p[3]` 表示一个一维数组内存放着三个指针变量，分别是 `p[0]` 、 `p[1]` 、 `p[2]` 
所以要分别赋值。

### 小结

这样两者的区别就豁然开朗了：

1. **数组指针只是一个指针变量**，似乎是C语言里**专门用来指向二维数组的**，它占有内存中一个指针的存储空间。
2. **指针数组是多个指针变量**，以数组形式存在内存当中，占有多个指针的存储空间。

还需要说明的一点就是，用来指向二维数组时，其引用和用数组名引用都是一样的。比如要表示数组p中*i行j列*一个元素： `*(p[i]+j)、*(*(p+i)+j)、(*(p+i))[j]、p[i][j]` 

优先级： `()>[]>*` 

> 资料来自：https://www.cnblogs.com/hongcha717/archive/2010/10/24/1859780.html

## 命令行参数

C/C++语言中的main函数，经常带有参数 `argc，argv` ，如下：

``` cpp
int main(int argc, char** argv)
int main(int argc, char* argv[])
```

C语言还规定 `argc` （第一个形参）必须是整型变量， `argv` （第二个形参）必须是指向字符串的指针数组。 

由于main函数不能被其它函数调用，因此不可能在程序内部取得实际值。那么，在何处把实参值赋予main函数的形参呢？实际上，main函数的参数值是从操作系统命令行上获得的。如何在操作系统命令行获取参数呢？

1. 在VS中设置时右键项目->属性->调试->命令参数，在命令参数中添加所需参数，字符串之间用空格分开即可。如果是 `.txt` 文件，要放在当前目录下（ `.cpp` 所在目录），不然找不到。
2. 或者：假如你的程序是 `hello.exe` ，如果在命令行运行该程序，（首先应该在命令行下用 `cd` 命令进入到 `hello.exe` 文件所在目录）运行命令为： `hello.exe data.txt` 

但是应该特别注意的是，main 的两个形参和命令行中的参数在位置上不是一一对应的。因为，main的形参只有二个，而命令行中的参数个数原则上未加限制。 `argc` 参数表示了命令行中参数的个数（注意：文件名本身也算一个参数）， `argc` 的值是在输入命令行时由系统按实际参数的个数自动赋予的。

