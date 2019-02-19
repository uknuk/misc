
# solutions to various algorithmic problems

def prime?(x)

  if x % 2 == 0
    puts 'No prime, divisible by 2'
    return false
  end

  3.step(Math.sqrt(x).floor, 2) do |i|
    if x % i == 0
      puts "No prime, divisible by #{i}"
      return false
    end
  end

  puts 'Prime'
  true
end

def unirand_arr(nMax)
  x = []
  nMax.times do
    begin
      n = rand(nMax) + 1
    end while x.include?(n)
    x << n
  end
  x
end

def qsort(arr)
  sz = arr.size
  return arr if sz <= 1
  idx = rand(sz)
  pivot = arr[idx]
  arr.delete_at(idx)
  # pivot = arr.shift
  left, right = arr.partition {|n| n < pivot}
  qsort(left) + [pivot] + qsort(right)
end

def ones(x)
  x.to_s(2).split(//).reduce(0) {|ones,n| ones + n.to_i}
end

def fib(x)
  return x if x < 2
  fib = [0,1,0] # n, n-1, n-2
  2.upto(x) do |k|
    fib[0] = fib[1] + fib[2]
    fib[1], fib[2] = fib[0], fib[1]
 end
 fib[0]
end

def balansed?(txt)
  par = {')' => '(', ']' => '[', '}' => '{'}
  left = par.values
  right = par.keys
  stack = []
  txt.split(//).each do |chr|
    if left.include? chr
      stack.push(chr)
    elsif right.include? chr
      if stack.size == 0
        puts 'right without left'
        return false
      elsif stack.last == par[chr]
        stack.pop
      else
        puts 'wrong right'
        return false
      end
    end
  end
  return stack.size == 0
end

def find2uniq(arr)
  xor = arr.reduce(&:^)
  puts "xor #{xor.to_s(2)}"
  puts "~(xor - 1) #{(~(xor - 1)).to_s(2)}"
  mask = xor & ~(xor - 1)
  puts mask.to_s(2)

  x = y = 0
  arr.each {|el| el & mask != 0 ? x ^= el : y ^= el}

  puts x,y
end
